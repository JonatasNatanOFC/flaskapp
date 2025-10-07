from flask import Flask, request, jsonify
from models.InstituicaoEnsino import InstituicaoEnsino
from utils.LoaderData import loadIE
from models.Usuario import Usuario

app = Flask(__name__)

usuarios = [
    Usuario("12345678900", "Natan Silva", "1990-01-01").to_json(),
    Usuario("98765432100", "Maria Souza", "1985-05-15").to_json()
]
instituicoesEnsino = []
ieData = loadIE()
for ie in ieData:
    ie = InstituicaoEnsino(
        ie['codigo'],
        ie['nome'],
        ie['co_uf'],
        ie['co_municipio'],
        ie['qt_mat_bas'],
        ie['qt_mat_prof'],
        ie['qt_mat_esp']
    ).to_json()
    instituicoesEnsino.append(ie)


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

    usuario = {"cpf": data["cpf"], "nome": data['nome'],
               "data_nascimento": data['data_nascimento']}
    usuarios.append(usuario)

    return usuario, 201


@app.get("/instituicoesensino")
def getInstituicoesEnsino():
    return instituicoesEnsino, 200


@app.post("/instituicoesensino")
def criarIE():
    data = request.get_json()

    ie = InstituicaoEnsino(
        data['codigo'],
        data['nome'],
        data['co_uf'],
        data['co_municipio'],
        data['qt_mat_bas'],
        data['qt_mat_prof'],
        data['qt_mat_esp']
    ).to_json()
    instituicoesEnsino.append(ie)

    return ie, 201


@app.put("/instituicoesensino/<int:id>")
def atualizarIE(id: int):
    data = request.get_json()

    ie = InstituicaoEnsino(
        data['codigo'],
        data['nome'],
        data['co_uf'],
        data['co_municipio'],
        data['qt_mat_bas'],
        data['qt_mat_prof'],
        data['qt_mat_esp']
    ).to_json()
    instituicoesEnsino[id] = ie

    return ie, 200


@app.delete("/instituicoesensino/<int:id>")
def deletarIE(id: int):
    instituicoesEnsino.pop(id)
    return '', 204


@app.get("/instituicoesensino/<int:id>")
def getInstituicoesEnsinoById(id: int):
    return instituicoesEnsino[id], 200
