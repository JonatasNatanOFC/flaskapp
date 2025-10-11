from flask import Flask, request, jsonify
from models.AgenteEconomico import AgenteEconomico
from models.Usuario import Usuario
from helpers.data import getAgentesEconomicos, loadUsuarios


app = Flask(__name__)


usuarios = loadUsuarios()
agentesEconomicos = getAgentesEconomicos()


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


@app.get("/agenteseconomicos")
def getAgentesEconomicos():
    return agentesEconomicos, 200


@app.post("/agenteseconomicos")
def criarAE():
    data = request.get_json()

    agente = AgenteEconomico(data).to_json()
    agentesEconomicos.append(agente)

    return agente, 201


@app.put("/agenteseconomicos/<int:id>")
def atualizarAE(id: int):
    data = request.get_json()
    agente = AgenteEconomico(data).to_json()
    agentesEconomicos[id] = agente
    return agente, 200


@app.delete("/agenteseconomicos/<int:id>")
def deletarAE(id: int):
    agentesEconomicos.pop(id)
    return '', 204


@app.get("/agenteseconomicos/<int:id>")
def getAgenteEconomicoById(id: int):
    return agentesEconomicos[id], 200


# buscar por id instituição de ensino e usuário;
