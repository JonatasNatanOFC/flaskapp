import json
from models.InstituicaoEnsino import InstituicaoEnsino
from models.Usuario import Usuario


def getInstituicoesEnsino():

    instituicoesEnsino = []

    with open('data/instituicoes.json', 'r', encoding='utf-8') as file:
        instituicoesEnsinoJson = json.load(file)

    for instituicaoEnsinoJson in instituicoesEnsinoJson:
        ie = InstituicaoEnsino(
            instituicaoEnsinoJson['CODIGO_DA_IES'],
            instituicaoEnsinoJson['NOME_DA_IES'],
            instituicaoEnsinoJson['SIGLA'],
            instituicaoEnsinoJson['CATEGORIA_DA_IES'],
            instituicaoEnsinoJson['COMUNITARIA'],
            instituicaoEnsinoJson['CONFESSIONAL'],
            instituicaoEnsinoJson['FILANTROPICA'],
            instituicaoEnsinoJson['ORGANIZACAO_ACADEMICA'],
            instituicaoEnsinoJson['CODIGO_MUNICIPIO_IBGE'],
            instituicaoEnsinoJson['MUNICIPIO'],
            instituicaoEnsinoJson['UF'],
            instituicaoEnsinoJson['SITUACAO_IES']
        )
        instituicoesEnsino.append(ie.to_json())
    return instituicoesEnsino


def loadUsuarios():

    with open('data/usuarios.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        usuarios = [Usuario(item['id'], item['nome'], item['cpf'],
                            item['data_nascimento']).to_json() for item in data]
        return usuarios
