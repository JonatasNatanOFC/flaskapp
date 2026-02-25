<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS tb_instituicao (
        id SERIAL PRIMARY KEY,
        codigo TEXT NOT NULL,
        nome TEXT NOT NULL,
        co_uf INTEGER NOT NULL,
        co_municipio INTEGER NOT NULL,
        qt_mat_bas INTEGER NOT NULL,
        qt_mat_prof INTEGER NOT NULL,
        qt_mat_esp INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_usuario (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL,
        nascimento DATE NOT NULL
=======
DROP TABLE IF EXISTS entidades;
DROP TABLE IF EXISTS tb_usuario;

CREATE TABLE entidades (
    CO_ENTIDADE INTEGER PRIMARY KEY,
    NO_MUNICIPIO TEXT,
    NO_ENTIDADE TEXT NOT NULL,
    SG_UF TEXT,
    QT_MAT_BAS INTEGER,
    QT_MAT_INF INTEGER,
    QT_MAT_FUND INTEGER,
    QT_MAT_MED INTEGER,
    QT_MAT_MED_CT INTEGER,
    QT_MAT_MED_NM INTEGER,
    QT_MAT_PROF INTEGER,
    QT_MAT_PROF_TEC INTEGER,
    QT_MAT_EJA INTEGER,
    QT_MAT_ESP INTEGER
);

CREATE TABLE tb_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    nascimento TEXT
>>>>>>> parent of 1fb7e74 (:sparkles: feat: Feito ranking dos ultimos 3 anos)
);