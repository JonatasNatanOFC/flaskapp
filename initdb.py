import sqlite3

DATABASE_NAME = 'censoescolar.db'


def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    with open('schema.sql') as f:
        print("Criando tabelas no banco de dados...")
        conn.executescript(f.read())

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
