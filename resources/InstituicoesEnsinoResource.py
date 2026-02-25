from flask import request
from flask_restful import Resource
from psycopg2 import Error
from psycopg2.extras import RealDictCursor  # Para facilitar o mapeamento
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.InstituicaoEnsino import InstituicaoEnsinoSchema


class InstituicoesEnsinoResources(Resource):
    def get(self):
        logger.info("get - /instituicoesensino")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            statement = "SELECT id, codigo, nome FROM tb_instituicao"
            cursor.execute(statement)
            resultset = cursor.fetchall()

            schema = InstituicaoEnsinoSchema(many=True)
            return schema.dump(resultset), 200

        except Error as e:
            logger.error(f"SQL Error: {e}")
            return {"mensagem": "Problema na operação com os dados"}, 500
        finally:
            if conn:
                conn.close()


class InstituicaoEnsinoResource(Resource):
    def get(self, id):
        logger.info(f"get - /instituicoesensino/{id}")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            statement = "SELECT id, codigo, nome FROM tb_instituicao WHERE id = %s"
            cursor.execute(statement, (id,))
            result = cursor.fetchone()

            if result is None:
                return {"mensagem": "Instituição de ensino não encontrada"}, 404

            schema = InstituicaoEnsinoSchema()
            return schema.dump(result), 200

        except Error as e:
            logger.error(f"SQL Error: {e}")
            return {"mensagem": "Problema na operação com os dados"}, 500
        finally:
            if conn:
                conn.close()
