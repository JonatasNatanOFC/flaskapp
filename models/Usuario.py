class Usuario():
    def __init__(self, cpf: str, nome: str, data_nascimento: str):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def __repr__(self):
        return f"<Usuario {self.nome}>"
    
    def to_json(self):
        return {
            "id": self.cpf,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento
        }
