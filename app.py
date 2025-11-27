import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

from helpers.logging import logger


app = Flask(__name__)
DATABASE_NAME = "censoescolar.db"


def get_db_conn():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def is_data_valida(data_string):
    try:
        datetime.strptime(data_string, '%Y-%m-%d')
        return True
    except ValueError:
        logger.warning(f"Data inválida recebida: {data_string}")
        return False


@app.get("/")
def index():
    logger.info("GET - /")
    return jsonify({
        "api": "Censo Escolar API",
        "versao": "2.1",
        "status": "online",
        "endpoints": ["/usuarios", "/instituicoesensino"]
    }), 200


@app.get("/usuarios")
def getUsuarios():
    logger.info("GET - /usuarios")
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM tb_usuario")
        usuarios = [dict(row) for row in cursor.fetchall()]
        return jsonify(usuarios), 200
    except sqlite3.OperationalError:
        logger.error("Tabela de usuários não encontrada no banco de dados.")
        return jsonify({"erro": "Tabela de usuários não encontrada. Execute init_db.py"}), 500
    finally:
        conn.close()


@app.get("/usuarios/<int:id>")
def getUsuariosById(id: int):
    logger.info(f"GET - /usuarios/{id}")

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_usuario WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify(dict(usuario)), 200
    logger.warning(f"Usuário não encontrado: ID {id}")
    return jsonify({"mensagem": "Usuário não encontrado"}), 404


@app.post("/usuarios")
def setUsuario():
    logger.info("POST - /usuarios")

    data = request.get_json()

    nome = data.get('nome')
    cpf = data.get('cpf')
    nascimento = data.get('nascimento')

    if not nome:
        logger.warning("Nome do usuário não fornecido na requisição.")
        return jsonify({"mensagem": "Nome é obrigatório"}), 400
    if not cpf or len(cpf) != 11:
        logger.warning("CPF inválido fornecido na requisição.")
        return jsonify({"mensagem": "CPF inválido (requer 11 dígitos)"}), 400
    if nascimento and not is_data_valida(nascimento):
        logger.warning(f"Data de nascimento inválida fornecida: {nascimento}")
        return jsonify({"mensagem": "Data inválida. Use YYYY-MM-DD"}), 400

    conn = get_db_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO tb_usuario (nome, cpf, nascimento) VALUES (?, ?, ?)",
            (nome, cpf, nascimento)
        )
        conn.commit()
        data['id'] = cursor.lastrowid
        return jsonify(data), 201
    except sqlite3.IntegrityError:
        logger.error(f"CPF já cadastrado: {cpf}")
        return jsonify({"mensagem": "CPF já cadastrado."}), 409
    except Exception as e:
        logger.error(f"Erro ao inserir usuário: {str(e)}")
        return jsonify({"mensagem": f"Erro interno: {str(e)}"}), 500
    finally:
        conn.close()


@app.get("/instituicoesensino")
def getInstituicoesEnsino():
    logger.info("GET - /instituicoesensino")

    conn = get_db_conn()
    cursor = conn.cursor()

    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 50, type=int)

        if limit > 1000:
            limit = 1000

        offset = (page - 1) * limit

        cursor.execute(
            "SELECT * FROM entidades LIMIT ? OFFSET ?", (limit, offset))
        entidades = [dict(row) for row in cursor.fetchall()]

        return jsonify({
            "pagina_atual": page,
            "itens_por_pagina": limit,
            "dados": entidades
        }), 200
    except Exception as e:
        logger.error(f"Erro ao buscar instituições de ensino: {str(e)}")
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.close()


@app.get("/instituicoesensino/<int:id>")
def getInstituicoesEnsinoById(id: int):
    logger.info(f"GET - /instituicoesensino/{id}")
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entidades WHERE CO_ENTIDADE = ?", (id,))
    entidade = cursor.fetchone()
    conn.close()

    if entidade:
        return jsonify(dict(entidade)), 200
    logger.warning(f"Instituição de ensino não encontrada: {id}")
    return jsonify({"mensagem": "Instituição não encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
