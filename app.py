from flask import Flask, request, jsonify
from models.InstituicaoEnsino import InstituicaoEnsino
from models.Usuario import Usuario
from helpers.data import  getInstituicoesEnsino, loadUsuarios


app = Flask(__name__)


usuarios = loadUsuarios()
instituicoesEnsino = getInstituicoesEnsino()

@app.get("/")
def index():
    return '{"versao":"2.0.0"}', 200


@app.get("/usuarios")
def getUsuarios():
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
    return  instituicoesEnsino, 200


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


