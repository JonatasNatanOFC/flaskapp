from marshmallow import Schema, fields
from sqlalchemy.orm import Mapped, mapped_column

from helpers.database import db


class InstituicaoEnsino(db.Model):

    __tablename__ = "tb_instituicao"
    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str] = mapped_column()
    co_uf: Mapped[int] = mapped_column()
    co_municipio: Mapped[int] = mapped_column()
    qt_mat_bas: Mapped[int] = mapped_column()
    qt_mat_prof: Mapped[int] = mapped_column()
    qt_mat_eja: Mapped[int] = mapped_column()
    qt_mat_esp: Mapped[int] = mapped_column()

    def __init__(self, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp):
        self.codigo = codigo
        self.nome = nome
        self.co_uf = co_uf
        self.co_municipio = co_municipio
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp

    def __repr__(self):
        return f'<InstituicaoEnsino {self.codigo}>'

    def to_json(self):
        return {"codigo": self.codigo, "nome": self.nome}


class InstituicaoEnsinoSchema(Schema):
    id = fields.Int(dump_only=True)  # dump_only pois o banco gera o ID
    codigo = fields.Int(required=True)
    nome = fields.Str(required=True)
    co_uf = fields.Int()
    co_municipio = fields.Int()
    qt_mat_bas = fields.Int()
    qt_mat_prof = fields.Int()
    qt_mat_eja = fields.Int()
    qt_mat_esp = fields.Int()
