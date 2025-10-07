import json

with open('data/instituicoes_paraiba.json', 'r') as f:
    instituicoes_ensino = json.load(f)

def loadIE():

    return instituicoes_ensino
