import json
from models.AgenteEconomico import AgenteEconomico
from models.Usuario import Usuario


def getAgentesEconomicos():

    with open('data/agentes_economicos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        agentes = [AgenteEconomico(item).to_json() for item in data]
    return agentes


def loadUsuarios():

    with open('data/usuarios.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        usuarios = [Usuario(item['id'],item['nome'], item['cpf'],
                            item['data_nascimento']).to_json() for item in data]
        return usuarios
