from flask import request
from flask_restful import Resource
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import get_conn
from models.Usuario import UsuarioSchema, Usuario
Resource


class UsuariosResource(Resource):
    def get(self):
        logger.info("get - /usuarios")
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id, nome, cpf, nascimento FROM tb_usuario")
            resultset = cursor.fetchall()

            # Serializa a lista de dicionários (resolve o erro da data)
            schema = UsuarioSchema(many=True)
            return schema.dump(resultset), 200

        except Error as e:
            logger.error(f"Erro SQL: {e}")
            return {"mensagem": "Problema na operação com os dados"}, 500
        finally:
            if conn:
                conn.close()

    def post(self):
        logger.info("post - /usuarios")
        conn = None
        try:
            usuario_json = request.get_json()
            data = UsuarioSchema().load(usuario_json)

            conn = get_conn()
            cursor = conn.cursor()

            query = "INSERT INTO tb_usuario (nome, cpf, nascimento) VALUES (%s, %s, %s) RETURNING id"
            cursor.execute(
                query, (data['nome'], data['cpf'], data['nascimento']))

            new_id = cursor.fetchone()[0]
            conn.commit()

            data['id'] = new_id
            return data, 201

        except ValidationError as err:
            return err.messages, 400
        except Error as e:
            logger.error(f"Erro SQL: {e}")
            return {"mensagem": "Erro ao inserir"}, 500
        finally:
            if conn:
                conn.close()


class UsuarioResource(Resource):
    def get(self, id):
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM tb_usuario WHERE id = %s", (id,))
            row = cursor.fetchone()

            if not row:
                return {"mensagem": "Não encontrado"}, 404

            return UsuarioSchema().dump(row), 200
        except Error as e:
            return {"mensagem": str(e)}, 500
        finally:
            if conn:
                conn.close()

    def delete(self, id):
        conn = None
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tb_usuario WHERE id = %s", (id,))
            conn.commit()
            return {"mensagem": "Excluído!"}, 200
        except Error as e:
            return {"mensagem": str(e)}, 500
        finally:
            if conn:
                conn.close()