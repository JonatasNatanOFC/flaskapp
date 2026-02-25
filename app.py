import sqlite3

from helpers.application import app, api
from helpers.database import get_conn
from helpers.logging import logger

from resources.HomeResource import HomeResources
from resources.UsuariosResource import UsuariosResource, UsuarioResource

api.add_resource(HomeResources, '/')
api.add_resource(UsuariosResource, '/usuarios')
api.add_resource(UsuarioResource, '/usuarios/<string:id>')


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

    logger.info("get - /instituicoesensino")
    try:
        # conectar com o banco.
        conn = get_conn()

        # capturar o cursor
        cursor = conn.cursor()

        # consultar: execução da dml.
        statement = "SELECT * FROM tb_instituicao"
        cursor.execute(statement)

        # fetch
        resultset = cursor.fetchall()

        instituicoesEnsinoResponse = []
        for row in resultset:
            id = row["id"]
            codigo = row["codigo"]
            nome = row["nome"]
            instituicaoEnsino = {"id": id, "codigo": codigo, "nome": nome}
            instituicoesEnsinoResponse.append(instituicaoEnsino)

        return instituicoesEnsinoResponse, 200

    except sqlite3.Error as e:
        logger.error(f"An SQLite error occurred: {e}")
        return {"mensagem": "Problema na operação com os dados"}, 500

# TODO: Implementar a migração para flask-restful


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
