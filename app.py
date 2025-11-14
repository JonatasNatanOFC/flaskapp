import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
DATABASE_NAME = "censoescolar.db"


def get_db_conn():
    """Cria uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_NAME)
    # Retorna linhas como dicionários (muito mais fácil que índices!)
    conn.row_factory = sqlite3.Row
    return conn


def is_data_valida(data_string):
    """Verifica se uma data está no formato YYYY-MM-DD."""
    try:
        datetime.strptime(data_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


@app.get("/")
def index():
    return jsonify({"versao": "2.0.0"}), 200

# --- Endpoints de Usuários ---


@app.get("/usuarios")
def getUsuarios():
    """Busca todos os usuários no banco de dados."""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_usuario")
    usuarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(usuarios), 200


@app.get("/usuarios/<int:id>")
def getUsuariosById(id: int):
    """Busca um usuário específico por ID."""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_usuario WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify(dict(usuario)), 200
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404


@app.post("/usuarios")
def setUsuario():
    """Cria um novo usuário."""
    usuarioJson = request.get_json()

    # Validação dos dados
    nome = usuarioJson.get('nome')
    # Permite espaços no nome
    if not nome or not nome.replace(' ', '').isalpha():
        return jsonify({"mensagem": "O nome do usuário é inválido!"}), 400

    cpf = usuarioJson.get('cpf')
    if not cpf or len(cpf) != 11 or not cpf.isdigit():  # Deve ter 11 dígitos
        return jsonify({"mensagem": "O cpf do usuário é inválido!"}), 400

    nascimento = usuarioJson.get('nascimento')
    if not is_data_valida(nascimento):  # CORREÇÃO: Lógica invertida
        return jsonify({"mensagem": "A data de nascimento do usuário é inválida! Use YYYY-MM-DD"}), 400

    # Manipulação com o banco de dados
    conn = get_db_conn()
    cursor = conn.cursor()

    try:
        # CORREÇÃO: Inserindo na tabela 'tb_usuario'
        statement = "INSERT INTO tb_usuario(nome, cpf, nascimento) VALUES (?, ?, ?)"
        cursor.execute(statement, (nome, cpf, nascimento))
        conn.commit()

        id_criado = cursor.lastrowid
        usuarioJson.update({"id": id_criado})

        return jsonify(usuarioJson), 201

    except sqlite3.IntegrityError:
        # Isso acontece se o CPF for duplicado
        return jsonify({"mensagem": "Erro: CPF já cadastrado."}), 409
    except Exception as e:
        conn.rollback()
        return jsonify({"mensagem": f"Erro interno: {e}"}), 500
    finally:
        conn.close()

# --- Endpoints das Instituições de Ensino ---


@app.get("/instituicoesensino")
def getInstituicoesEnsino():
    """Busca todas as instituições no banco (usando o row_factory)."""
    conn = get_db_conn()
    cursor = conn.cursor()

    # Paginação simples (opcional, mas recomendado)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 50, type=int)
    offset = (page - 1) * limit

    cursor.execute("SELECT * FROM entidades LIMIT ? OFFSET ?", (limit, offset))

    # Converte o resultado para uma lista de dicionários
    entidades = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify(entidades), 200


@app.get("/instituicoesensino/<int:id>")
def getInstituicoesEnsinoById(id: int):
    """Busca uma instituição específica pelo CO_ENTIDADE."""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entidades WHERE CO_ENTIDADE = ?", (id,))
    entidade = cursor.fetchone()
    conn.close()

    if entidade:
        return jsonify(dict(entidade)), 200
    else:
        return jsonify({"mensagem": "Instituição não encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
