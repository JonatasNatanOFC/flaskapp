import sqlite3

DATABASE_NAME = 'censoescolar.db'

tables = [
    '''CREATE TABLE IF NOT EXISTS tb_instituicao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_ies INTEGER NOT NULL,
        nome_ies TEXT NOT NULL,
        sigla TEXT,
        categoria_ies TEXT NOT NULL,
        comunitaria TEXT NOT NULL,
        confessional TEXT NOT NULL,
        filantropica TEXT NOT NULL,
        organizacao_academica TEXT NOT NULL,
        codigo_municipio_ibge TEXT NOT NULL,
        municipio TEXT NOT NULL,
        uf TEXT NOT NULL,
        situacao_ies TEXT NOT NULL
    );''',
    '''CREATE TABLE IF NOT EXISTS tb_usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL,
        data_nascimento DATE NOT NULL
    );'''
]


def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    for table in tables:
        cursor.execute(table)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
