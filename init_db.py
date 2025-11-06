import json
import sqlite3

DATABASE_NAME = 'censoescolar.db'
SCHEMA = 'schema.sql'
instituicoesJson = './data/instituicoes.json'
usuariosJson = './data/usuarios.json'


def create_tables():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        print(f"Executando Schema de '{SCHEMA}'...")
        with open(SCHEMA, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
        print("Tabelas criadas com sucesso.")

        print(f"Lendo dados de '{instituicoesJson}'...")
        with open(instituicoesJson, 'r', encoding='utf-8') as f:
            instituicoes_data = json.load(f)

            sql_insert = '''INSERT INTO tb_instituicao (
                codigo_ies, nome_ies, sigla, categoria_ies, comunitaria,
                confessional, filantropica, organizacao_academica,
                codigo_municipio_ibge, municipio, uf, situacao_ies) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )'''

            count = 0
            for instituicao in instituicoes_data:
                try:
                    codigo_ies = instituicao['CODIGO_DA_IES']
                    nome_ies = instituicao['NOME_DA_IES']
                    sigla = instituicao['SIGLA']
                    categoria_ies = instituicao['CATEGORIA_DA_IES']
                    comunitaria = instituicao['COMUNITARIA']
                    confessional = instituicao['CONFESSIONAL']
                    filantropica = instituicao['FILANTROPICA']
                    organizacao_academica = instituicao['ORGANIZACAO_ACADEMICA']
                    codigo_municipio_ibge = instituicao['CODIGO_MUNICIPIO_IBGE']
                    municipio = instituicao['MUNICIPIO']
                    uf = instituicao['UF']
                    situacao_ies = instituicao['SITUACAO_IES']
                    cursor.execute(sql_insert, (
                        codigo_ies, nome_ies, sigla, categoria_ies, comunitaria,
                        confessional, filantropica, organizacao_academica,
                        codigo_municipio_ibge, municipio, uf, situacao_ies
                    ))
                    count += 1
                except KeyError:
                    print(
                        f"AVISO: Item no Json está mal formatado (faltando chave) {instituicao}")
                except sqlite3.IntegrityError:
                    print(
                        f"AVISO: Instituição com código_ies {codigo_ies} já existe no banco de dados. Ignorando inserção duplicada.")

            print(f"{count} instituições inseridas com sucesso.")
        with open(usuariosJson, 'r', encoding='utf-8') as f:
            usuarios_data = json.load(f)
            sql_insert_usuario = '''INSERT INTO tb_usuario (
                nome, cpf, data_nascimento) VALUES ( ?, ?, ? )'''
            count_usuarios = 0
            for usuario in usuarios_data:
                try:
                    nome = usuario['nome']
                    cpf = usuario['cpf']
                    data_nascimento = usuario['data_nascimento']
                    cursor.execute(sql_insert_usuario, (
                        nome, cpf, data_nascimento
                    ))
                    count_usuarios += 1
                except KeyError:
                    print(
                        f"AVISO: Item no Json está mal formatado (faltando chave) {usuario}")
                except sqlite3.IntegrityError:
                    print(
                        f"AVISO: Usuário com CPF {cpf} já existe no banco de dados. Ignorando inserção duplicada.")
            print(f"{count_usuarios} usuários inseridos com sucesso.")

            conn.commit()
            print(
                f"Banco de dados '{DATABASE_NAME}' inicializado com sucesso.")
    except sqlite3.Error as e:
        print(f"Ocorreu um erro geral do SQLite: {e}")
    except FileNotFoundError:
        print(
            f"Erro: Arquivo '{SCHEMA}' ou '{instituicoesJson}' não encontrado.")
    except json.JSONDecodeError:
        print(f"Erro: o Arquivo '{instituicoesJson}' não é um JSON válido.")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_tables()
