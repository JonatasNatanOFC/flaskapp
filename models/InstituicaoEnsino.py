class InstituicaoEnsino():

    def __init__(self, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_esp):
        self.codigo = codigo
        self.nome = nome
        self.co_uf = co_uf
        self.co_municipio = co_municipio
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_esp = qt_mat_esp

    def __repr__(self):
        return f"<InstituicaoEnsino {self.nome}>"

    def to_json(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "co_uf": self.co_uf,
            "co_municipio": self.co_municipio,
            "qt_mat_bas": self.qt_mat_bas,
            "qt_mat_prof": self.qt_mat_prof,
            "qt_mat_esp": self.qt_mat_esp
        }


# dar carga das instituições de ensino a partir de um arquivo JSON;
# implementar metodo post put e delete para instituicoes de ensino;
# criar a modelo usario, com nome, cpf e data de 