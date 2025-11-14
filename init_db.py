import pandas as pd
import sqlite3
import sys
import os

DATABASE_NAME = "censoescolar.db"
CSV_FILE = os.path.join("data", "microdados_ed_basica_2024.csv")
SCHEMA_FILE = "schema.sql"
FILTRO_REGIAO = "NORDESTE"

COLUNAS_PARA_LER = [
    'CO_ENTIDADE',
    'NO_MUNICIPIO',
    'NO_ENTIDADE',
    'SG_UF',
    'QT_MAT_BAS',
    'QT_MAT_INF',
    'QT_MAT_FUND',
    'QT_MAT_MED',
    'QT_MAT_MED_CT',
    'QT_MAT_MED_NM',
    'QT_MAT_PROF',
    'QT_MAT_PROF_TEC',
    'QT_MAT_EJA',
    'QT_MAT_ESP',
    'NO_REGIAO'
]

COLUNAS_PARA_SALVAR = [
    'CO_ENTIDADE',
    'NO_MUNICIPIO',
    'NO_ENTIDADE',
    'SG_UF',
    'QT_MAT_BAS',
    'QT_MAT_INF',
    'QT_MAT_FUND',
    'QT_MAT_MED',
    'QT_MAT_MED_CT',
    'QT_MAT_MED_NM',
    'QT_MAT_PROF',
    'QT_MAT_PROF_TEC',
    'QT_MAT_EJA',
    'QT_MAT_ESP'
]


def setup_database():
    print(f"Iniciando configuração do banco: {DATABASE_NAME}")
    if not os.path.exists(SCHEMA_FILE):
        print(f"Erro: Arquivo {SCHEMA_FILE} não encontrado.")
        return False

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        with open(SCHEMA_FILE) as f:
            cursor.executescript(f.read())
        conn.commit()
        print("Tabela 'entidades' criada com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao executar {SCHEMA_FILE}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def populate_data():
    print(f"Iniciando carga de dados do CSV: {CSV_FILE}")
    if not os.path.exists(CSV_FILE):
        print(f"Erro: Arquivo {CSV_FILE} não encontrado.")
        print("Por favor, baixe o arquivo e coloque-o na pasta 'data'.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    total_inserido = 0

    try:
        tamanho_chunk = 100000

        csv_iterator = pd.read_csv(
            CSV_FILE,
            encoding='latin1',
            delimiter=';',
            usecols=COLUNAS_PARA_LER,
            chunksize=tamanho_chunk
        )

        print(f"Iniciando filtro para a região: {FILTRO_REGIAO}")

        for i, chunk_df in enumerate(csv_iterator):
            sys.stdout.write(f"\rProcessando chunk {i+1}...")
            sys.stdout.flush()

            coluna_filtro_limpa = chunk_df["NO_REGIAO"].str.strip().str.upper()

            chunk_filtrado = chunk_df[coluna_filtro_limpa == FILTRO_REGIAO]

            if not chunk_filtrado.empty:

                chunk_final = chunk_filtrado[COLUNAS_PARA_SALVAR]

                chunk_final = chunk_final.fillna(0)

                chunk_final.to_sql(
                    'entidades',
                    conn,
                    if_exists='append',
                    index=False
                )
                total_inserido += len(chunk_final)

        print(f"\n\nOperação finalizada!")
        print(
            f"Foram cadastradas {total_inserido} entidades da região {FILTRO_REGIAO}.")

    except Exception as e:
        print(f"\nOcorreu um erro durante a carga: {e}")
        print("Verifique se os nomes em 'COLUNAS_PARA_LER' estão corretos,")
        print("se o delimitador é ';' e se o encoding 'latin1' é o certo.")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    if setup_database():
        populate_data()
