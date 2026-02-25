import sqlite3

from helpers.application import app, api
from helpers.database import db, get_conn
from helpers.logging import logger

from resources.HomeResource import HomeResources
from resources.UsuariosResource import UsuariosResource, UsuarioResource
from resources.InstituicoesEnsinoResource import InstituicoesEnsinoResources, InstituicaoEnsinoResource

api.add_resource(HomeResources, '/')
api.add_resource(UsuariosResource, '/usuarios')
api.add_resource(UsuarioResource, '/usuarios/<string:id>')

api.add_resource(InstituicoesEnsinoResources, '/instituicoesensino')
api.add_resource(InstituicaoEnsinoResource, '/instituicoesensino/<string:id>')
