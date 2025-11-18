import pandas as pd
import sqlite3
import sys
import os
import json

DATABASE_NAME = "censoescolar.db"

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


def setup_database():
    print(f"--- Configurando Banco de Dados: {DATABASE_NAME} ---")
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if not os.path.exists(SCHEMA_FILE):
        print(f"Erro: {SCHEMA_FILE} não encontrado.")
        return False

    try:
        with open(SCHEMA_FILE, 'r') as f:
            cursor.executescript(f.read())
        conn.commit()
        print("Tabelas recriadas com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        return False
    finally:
        conn.close()


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

    conn = sqlite3.connect(DATABASE_NAME)
    total_inserido = 0

    try:
        csv_iterator = pd.read_csv(
            CSV_FILE, encoding='latin1', delimiter=';',
            usecols=COLUNAS_PARA_LER, chunksize=50000
        )

        print(f"Filtrando região: {FILTRO_REGIAO}")

        for i, chunk_df in enumerate(csv_iterator):
            # Filtro
            chunk_filtrado = chunk_df[chunk_df["NO_REGIAO"].str.strip(
            ).str.upper() == FILTRO_REGIAO]

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
    finally:
        conn.close()


if __name__ == "__main__":
    if setup_database():
        populate_from_csv()
