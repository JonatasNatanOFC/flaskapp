<<<<<<< HEAD
<<<<<<< HEAD
import psycopg2
from psycopg2 import OperationalError

DATABASE_NAME = "censoescolar.db"
=======
import pandas as pd
import sqlite3
import sys
import os
import json

DATABASE_NAME = "censoescolar.db"
=======
import pandas as pd
import sqlite3
import sys
import os
import json

DATABASE_NAME = "censoescolar.db"
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)

# Caminhos dos arquivos
CSV_FILE = os.path.join("data", "microdados_ed_basica_2024.csv")
JSON_FILE = os.path.join("data", "instituicoesensino.json")
SCHEMA_FILE = "schema.sql"

FILTRO_REGIAO = "NORDESTE"

COLUNAS_PARA_LER = [
    'CO_ENTIDADE', 'NO_MUNICIPIO', 'NO_ENTIDADE', 'SG_UF',
    'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND', 'QT_MAT_MED',
    'QT_MAT_MED_CT', 'QT_MAT_MED_NM', 'QT_MAT_PROF',
    'QT_MAT_PROF_TEC', 'QT_MAT_EJA', 'QT_MAT_ESP', 'NO_REGIAO'
]

COLUNAS_DB = [
    'CO_ENTIDADE', 'NO_MUNICIPIO', 'NO_ENTIDADE', 'SG_UF',
    'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND', 'QT_MAT_MED',
    'QT_MAT_MED_CT', 'QT_MAT_MED_NM', 'QT_MAT_PROF',
    'QT_MAT_PROF_TEC', 'QT_MAT_EJA', 'QT_MAT_ESP'
]
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)


def create_tables():
    try:
        print("Iniciando criação")

<<<<<<< HEAD
        conn = psycopg2.connect(
            dbname="censoescolar",
            user="pweb2",
            password="123456",
            host="localhost",
            port="5434"
=======

def populate_from_json():
    print(f"\n--- Iniciando carga via JSON: {JSON_FILE} ---")
    if not os.path.exists(JSON_FILE):
        print(f"Arquivo JSON não encontrado em {JSON_FILE}. Pulando etapa.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)

        contador = 0
        for item in dados_json:
            cursor.execute("""
                INSERT OR IGNORE INTO entidades (
                    CO_ENTIDADE, NO_ENTIDADE, SG_UF, NO_MUNICIPIO, 
                    QT_MAT_BAS, QT_MAT_PROF, QT_MAT_EJA, QT_MAT_ESP
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get("codigo"),
                item.get("nome"),
                item.get("co_uf"),
                item.get("co_municipio"),
                item.get("qt_mat_bas", 0),
                item.get("qt_mat_prof", 0),
                item.get("qt_mat_eja", 0),
                item.get("qt_mat_esp", 0)
            ))
            contador += 1

        conn.commit()
        print(f"Sucesso: {contador} registros inseridos via JSON.")

    except Exception as e:
        print(f"Erro na carga JSON: {e}")
        conn.rollback()
    finally:
        conn.close()


<<<<<<< HEAD
def populate_from_csv():
    print(f"\n--- Iniciando carga via CSV: {CSV_FILE} ---")
    if not os.path.exists(CSV_FILE):
        print("CSV não encontrado. Se quiser carga massiva, adicione o arquivo na pasta data/.")
        return

=======
def populate_from_json():
    print(f"\n--- Iniciando carga via JSON: {JSON_FILE} ---")
    if not os.path.exists(JSON_FILE):
        print(f"Arquivo JSON não encontrado em {JSON_FILE}. Pulando etapa.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)

        contador = 0
        for item in dados_json:
            cursor.execute("""
                INSERT OR IGNORE INTO entidades (
                    CO_ENTIDADE, NO_ENTIDADE, SG_UF, NO_MUNICIPIO, 
                    QT_MAT_BAS, QT_MAT_PROF, QT_MAT_EJA, QT_MAT_ESP
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get("codigo"),
                item.get("nome"),
                item.get("co_uf"),
                item.get("co_municipio"),
                item.get("qt_mat_bas", 0),
                item.get("qt_mat_prof", 0),
                item.get("qt_mat_eja", 0),
                item.get("qt_mat_esp", 0)
            ))
            contador += 1

        conn.commit()
        print(f"Sucesso: {contador} registros inseridos via JSON.")

    except Exception as e:
        print(f"Erro na carga JSON: {e}")
        conn.rollback()
    finally:
        conn.close()


def populate_from_csv():
    print(f"\n--- Iniciando carga via CSV: {CSV_FILE} ---")
    if not os.path.exists(CSV_FILE):
        print("CSV não encontrado. Se quiser carga massiva, adicione o arquivo na pasta data/.")
        return

>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
    conn = sqlite3.connect(DATABASE_NAME)
    total_inserido = 0

    try:
        csv_iterator = pd.read_csv(
            CSV_FILE, encoding='latin1', delimiter=';',
            usecols=COLUNAS_PARA_LER, chunksize=50000
<<<<<<< HEAD
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
=======
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
        )

        print(f"Filtrando região: {FILTRO_REGIAO}")

<<<<<<< HEAD
<<<<<<< HEAD
        with open('schema.sql') as f:
            print("Criando as tabelas")
            cursor.execute(f.read())

        print("Inserindo usuário padrão")
        cursor.execute("INSERT INTO tb_usuario (nome, cpf, nascimento) VALUES (%s, %s, %s)",
                       ('João da Silva', '00011122255', '2025-10-30'))
        conn.commit()

    except OperationalError as e:
        # Handle the error, print details, or log the error
        print(f"The connection failed: {e}")
        # Optional: Get the PostgreSQL error code
        if hasattr(e, 'pgcode'):
            print(f"PostgreSQL Error Code: {e.pgcode}")

    except psycopg2.Error as e:
        # Catch any other general psycopg2 errors
        print(f"A general psycopg2 error occurred: {e}")

=======
        for i, chunk_df in enumerate(csv_iterator):
            # Filtro
            chunk_filtrado = chunk_df[chunk_df["NO_REGIAO"].str.strip(
            ).str.upper() == FILTRO_REGIAO]

=======
        for i, chunk_df in enumerate(csv_iterator):
            # Filtro
            chunk_filtrado = chunk_df[chunk_df["NO_REGIAO"].str.strip(
            ).str.upper() == FILTRO_REGIAO]

>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
            if not chunk_filtrado.empty:
                chunk_final = chunk_filtrado[COLUNAS_DB].fillna(0)

                chunk_final.to_sql('entidades', conn,
                                   if_exists='append', index=False)

                registros_chunk = len(chunk_final)
                total_inserido += registros_chunk
                sys.stdout.write(
                    f"\rChunks processados: {i+1} | Registros inseridos: {total_inserido}")
                sys.stdout.flush()

        print(f"\nCarga CSV finalizada! Total de {total_inserido} registros.")

    except Exception as e:
        print(f"\nErro na carga CSV: {e}")
<<<<<<< HEAD
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
=======
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
    finally:
        print("Fechar conexão")
        conn.close()


if __name__ == "__main__":
<<<<<<< HEAD
    create_tables()
=======
    if setup_database():
        populate_from_csv()
<<<<<<< HEAD
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
=======
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
