import pandas as pd
import sqlite3

csv_file = "data/microdados_ed_basica_2024.csv"

colList = ['CO_ENTIDADE', 'CO_REGIAO', 'NO_REGIAO', 'NO_UF', 'SG_UF', 'NO_MUNICIPIO', 'NO_MESORREGIAO', 'NO_MICRORREGIAO', 'NO_ENTIDADE',
           'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND', 'QT_MAT_MED', 'QT_MAT_MED_CT', 'QT_MAT_MED_NM',
           'QT_MAT_PROF', 'QT_MAT_PROF_TEC', 'QT_MAT_EJA', 'QT_MAT_ESP']


data = pd.read_csv(csv_file, encoding='latin-1',
                   delimiter=';', usecols=colList)
filtro_data = data[data["NO_REGIAO"] == ('Nordeste')].fillna(0)

entidades = filtro_data.to_dict(orient='records')

entidades_info = [(entidade['CO_ENTIDADE'], entidade['CO_REGIAO'], entidade['NO_REGIAO'], entidade['NO_UF'], entidade['SG_UF'], entidade['NO_MUNICIPIO'],
                   entidade['NO_MESORREGIAO'], entidade['NO_MICRORREGIAO'], entidade[
                       'NO_ENTIDADE'], entidade['QT_MAT_BAS'], entidade['QT_MAT_INF'],
                   entidade['QT_MAT_FUND'], entidade['QT_MAT_MED'], entidade['QT_MAT_MED_CT'], entidade['QT_MAT_MED_NM'], entidade['QT_MAT_PROF'],
                   entidade['QT_MAT_PROF_TEC'], entidade['QT_MAT_EJA'], entidade['QT_MAT_ESP']
                   ) for entidade in entidades]

connection = sqlite3.connect('censoescolar.db')

cursor = connection.cursor()

with open('schema.sql') as file:
    cursor.executescript(file.read())


cursor.executemany(
    """insert into entidades(CO_ENTIDADE, CO_REGIAO, NO_REGIAO, NO_UF, SG_UF, NO_MUNICIPIO, 
    NO_MESORREGIAO, NO_MICRORREGIAO, NO_ENTIDADE, QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND, QT_MAT_MED, 
    QT_MAT_MED_CT, QT_MAT_MED_NM, QT_MAT_PROF, QT_MAT_PROF_TEC, QT_MAT_EJA, QT_MAT_ESP)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", entidades_info)

connection.commit()

connection.close()

print(f"Operação finalizada! Foram cadastradas {len(entidades)} Entidades.")
