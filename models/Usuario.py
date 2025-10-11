class Usuario():
    def __init__(self, id: int, nome: str, cpf: str, data_nascimento: str):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def to_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento
        }

    def __repr__(self):
        return f"Usuario({self.nome}, {self.cpf}, {self.data_nascimento})"
