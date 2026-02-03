from flask_restful import Resource


class HomeResources(Resource):
    def get(self):
        # Retorne um dicionário, não uma string
        return {"versao": "2.0.0"}, 200
