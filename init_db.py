import pandas as pd
import sqlite3
import glob
import os

DATABASE_NAME = "censoescolar.db"
SCHEMA_FILE = "schema.sql"

COLUNAS_DESEJADAS = [
    'NO_ENTIDADE', 'CO_ENTIDADE', 'NO_UF', 'SG_UF', 'CO_UF', 'NO_MUNICIPIO', 'CO_MUNICIPIO',
    'NO_MESORREGIAO', 'CO_MESORREGIAO', 'NO_MICRORREGIAO', 'CO_MICRORREGIAO', 'NU_ANO_CENSO',
    'NO_REGIAO', 'CO_REGIAO', 'QT_MAT_BAS', 'QT_MAT_PROF', 'QT_MAT_EJA', 'QT_MAT_ESP',
    'QT_MAT_FUND', 'QT_MAT_INF', 'QT_MAT_MED', 'QT_MAT_ZR_NA', 'QT_MAT_ZR_RUR', 'QT_MAT_ZR_URB'
]

COLUNAS_BASE_DB = [
    'NO_ENTIDADE', 'CO_ENTIDADE', 'NO_UF', 'SG_UF', 'CO_UF', 'NO_MUNICIPIO', 'CO_MUNICIPIO',
    'NO_MESORREGIAO', 'CO_MESORREGIAO', 'NO_MICRORREGIAO', 'CO_MICRORREGIAO', 'NU_ANO_CENSO',
    'NO_REGIAO', 'CO_REGIAO', 'QT_MAT_BAS', 'QT_MAT_PROF', 'QT_MAT_EJA', 'QT_MAT_ESP',
    'QT_MAT_FUND', 'QT_MAT_INF', 'QT_MAT_MED', 'QT_MAT_ZR_NA', 'QT_MAT_ZR_RUR', 'QT_MAT_ZR_URB'
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


def populate_from_csv(arquivo):
    print(f"\n--- Processando: {arquivo} ---")
    if not os.path.exists(arquivo):
        return

    try:
        df_head = pd.read_csv(arquivo, encoding='latin1', sep=';', nrows=0)
        sep_usado = ';'
        if len(df_head.columns) < 2:
            df_head = pd.read_csv(arquivo, encoding='latin1', sep=',', nrows=0)
            sep_usado = ','
    except Exception as e:
        print(f"Erro ao ler cabeçalho: {e}")
        return

    cols_existentes = list(df_head.columns)
    cols_para_ler = [c for c in COLUNAS_DESEJADAS if c in cols_existentes]
    cols_faltantes = list(set(COLUNAS_DESEJADAS) - set(cols_para_ler))

    conn = sqlite3.connect(DATABASE_NAME)
    total_inserido = 0

    try:
        csv_iterator = pd.read_csv(
            arquivo, encoding='latin1', delimiter=sep_usado,
            usecols=cols_para_ler, chunksize=50000
        )

        cursor = conn.cursor()

        for chunk in csv_iterator:
            for col in cols_faltantes:
                chunk[col] = 0

            if 'QT_MAT_BAS' in chunk.columns:
                chunk['QT_MAT_TOTAL'] = chunk['QT_MAT_BAS']
            else:
                chunk['QT_MAT_TOTAL'] = 0

            chunk['NU_RANKING'] = 0

            cols_finais = COLUNAS_BASE_DB + ['QT_MAT_TOTAL', 'NU_RANKING']
            chunk = chunk[cols_finais]
            chunk.fillna(0, inplace=True)

            registros = chunk.to_records(index=False).tolist()

            placeholders = ','.join(['?'] * 26)
            colunas_sql = ','.join(cols_finais)

            cursor.executemany(f"""
                INSERT OR IGNORE INTO entidades ({colunas_sql}) 
                VALUES ({placeholders})
            """, registros)

            conn.commit()
            total_inserido += cursor.rowcount
            print(f"Lote inserido. Total acumulado: {total_inserido}")

    except Exception as e:
        print(f"Erro na carga: {e}")
    finally:
        conn.close()


def calcular_ranking_final():
    print("\n--- Calculando Ranking por Ano (SQL) ---")
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        sql_update = """
        UPDATE entidades
        SET NU_RANKING = r.rank_calc
        FROM (
            SELECT CO_ENTIDADE, NU_ANO_CENSO,
                   RANK() OVER (
                       PARTITION BY NU_ANO_CENSO 
                       ORDER BY QT_MAT_TOTAL DESC
                   ) as rank_calc
            FROM entidades
        ) AS r
        WHERE entidades.CO_ENTIDADE = r.CO_ENTIDADE 
          AND entidades.NU_ANO_CENSO = r.NU_ANO_CENSO;
        """

        print("Executando atualização de ranking anual...")
        cursor.execute(sql_update)
        conn.commit()
        print("Ranking calculado com sucesso!")

    except Exception as e:
        print(f"Erro ao calcular ranking: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    if setup_database():
        padrao_arquivos = os.path.join("data", "*.csv")
        lista_arquivos = glob.glob(padrao_arquivos)

        for arquivo_csv in lista_arquivos:
            populate_from_csv(arquivo_csv)

        calcular_ranking_final()
