class InstituicaoEnsino:
    def __init__(self, codigo_da_ies: int, nome_da_ies: str, sigla: str,
                 categoria_da_ies: str, comunitaria: str, confessional: str,
                 filantropica: str, organizacao_academica: str,
                 codigo_municipio_ibge: str, municipio: str, uf: str,
                 situacao_ies: str):
        self.codigo_da_ies = codigo_da_ies
        self.nome_da_ies = nome_da_ies
        self.sigla = sigla
        self.categoria_da_ies = categoria_da_ies
        self.comunitaria = comunitaria
        self.confessional = confessional
        self.filantropica = filantropica
        self.organizacao_academica = organizacao_academica
        self.codigo_municipio_ibge = codigo_municipio_ibge
        self.municipio = municipio
        self.uf = uf
        self.situacao_ies = situacao_ies

    def to_json(self):
        return {
            "CODIGO_DA_IES": self.codigo_da_ies,
            "NOME_DA_IES": self.nome_da_ies,
            "SIGLA": self.sigla,
            "CATEGORIA_DA_IES": self.categoria_da_ies,
            "COMUNITARIA": self.comunitaria,
            "CONFESSIONAL": self.confessional,
            "FILANTROPICA": self.filantropica,
            "ORGANIZACAO_ACADEMICA": self.organizacao_academica,
            "CODIGO_MUNICIPIO_IBGE": self.codigo_municipio_ibge,
            "MUNICIPIO": self.municipio,
            "UF": self.uf,
            "SITUACAO_IES": self.situacao_ies
        }

    def __repr__(self):
        return f"InstituicaoEducacional({self.nome_da_ies}, {self.categoria_da_ies}, {self.municipio})"