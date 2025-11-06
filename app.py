from flask import Flask, request, jsonify, abort
from models.InstituicaoEnsino import InstituicaoEnsino
from models.Usuario import Usuario
from helpers.data import getInstituicoesEnsino, loadUsuarios
import sqlite3


app = Flask(__name__)

DATABASE = 'censoescolar.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


usuarios = loadUsuarios()
instituicoesEnsino = getInstituicoesEnsino()


@app.get("/")
def index():
    return '{"versao":"2.0.0"}', 200


@app.get("/usuarios")
def getUsuarios():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_usuario")
    usuarios_rows = cursor.fetchall()
    conn.close()
    usuarios = [dict(row) for row in usuarios_rows]
    return jsonify(usuarios), 200


@app.get("/usuarios/<int:id>")
def getUsuariosById(id: int):
    return jsonify(usuarios[id])


@app.post("/usuarios")
def setUsuarios():
    data = request.get_json()

    usuario = Usuario(
        data['nome'],
        data['cpf'],
        data['data_nascimento']
    ).to_json()
    usuarios.append(usuario)

    return usuario, 201


@app.get("/instituicoesensino")
def getInstituicoesEnsino():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_instituicao")
    instituicoes_rows = cursor.fetchall()
    conn.close()
    instituicoes = [dict(row) for row in instituicoes_rows]
    return jsonify(instituicoes), 200


@app.post("/instituicoesensino")
def criarIE():
    data = request.get_json()

    ie = InstituicaoEnsino(data).to_json()
    instituicoesEnsino.append(ie)

    return ie, 201


@app.put("/instituicoesensino/<int:id>")
def atualizarIE(id: int):
    data = request.get_json()
    ie = InstituicaoEnsino(data).to_json()
    instituicoesEnsino[id] = ie
    return ie, 200


@app.delete("/instituicoesensino/<int:id>")
def deletarIE(id: int):
    instituicoesEnsino.pop(id)
    return '', 204


@app.get("/instituicoesensino/<int:id>")
def getInstituicaoEnsinoById(id: int):
    return instituicoesEnsino[id], 200
