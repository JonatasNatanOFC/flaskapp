class AgenteEconomico:
    def __init__(self, data: dict):
        self.data_inicio_representacao = data.get("DATA_INICIO_REPRESENTACAO")
        self.razao_social = data.get("RAZAO_SOCIAL")
        self.registro_representante = data.get("REGISTRO_REPRESENTANTE")
        self.representante = data.get("REPRESENTANTE")
        self.data_registro = data.get("DATA_REGISTRO")
        self.atividade_principal = data.get("ATIVIDADE_PRINCIPAL")
        self.registro_ancine = data.get("REGISTRO_ANCINE")
        self.cnpj_representante = data.get("CNPJ_REPRESENTANTE")
        self.data_final_representacao = data.get("DATA_FINAL_REPRESENTACAO")

    def to_json(self):
        return {
            "DATA_INICIO_REPRESENTACAO": self.data_inicio_representacao,
            "RAZAO_SOCIAL": self.razao_social,
            "REGISTRO_REPRESENTANTE": self.registro_representante,
            "REPRESENTANTE": self.representante,
            "DATA_REGISTRO": self.data_registro,
            "ATIVIDADE_PRINCIPAL": self.atividade_principal,
            "REGISTRO_ANCINE": self.registro_ancine,
            "CNPJ_REPRESENTANTE": self.cnpj_representante,
            "DATA_FINAL_REPRESENTACAO": self.data_final_representacao
        }

    def __repr__(self):
        return f"AgenteEconomico({self.razao_social}, {self.representante})"
