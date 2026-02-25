DROP TABLE IF EXISTS tb_instituicao;
DROP TABLE IF EXISTS tb_usuario;
CREATE TABLE IF NOT EXISTS tb_instituicao (
        id SERIAL PRIMARY KEY,
        codigo TEXT NOT NULL,
        nome TEXT NOT NULL,
        co_uf INTEGER NOT NULL,
        co_municipio INTEGER NOT NULL,
        qt_mat_bas INTEGER NOT NULL,
        qt_mat_prof INTEGER NOT NULL,
        qt_mat_eja INTEGER NOT NULL,
        qt_mat_esp INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_usuario (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL, 
        nascimento DATE NOT NULL
);
