CREATE DATABASE echocad_sql;
USE echocad_sql;

-- =========================
-- Tabela: Usuario
-- =========================
CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cargo VARCHAR(100)
);

-- =========================
-- Tabela: Projeto
-- =========================
CREATE TABLE Projeto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    cliente VARCHAR(150),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,

    id_usuario INT NOT NULL,

    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);

-- =========================
-- Tabela: Norma
-- =========================
CREATE TABLE Norma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    conexao VARCHAR(100),
    status VARCHAR(50),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- Tabela associativa: Projeto_Norma
-- (Relacionamento N:N "auxilia")
-- =========================
CREATE TABLE Projeto_norma (
    id_projeto INT,
    id_norma INT,

    PRIMARY KEY (id_projeto, id_norma),

    FOREIGN KEY (id_projeto) REFERENCES Projeto(id),
    FOREIGN KEY (id_norma) REFERENCES Norma(id)
);

-- =========================
-- Tabela: Planta_CAD
-- =========================
CREATE TABLE Planta_cad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100),
    arquivo VARCHAR(255),

    id_projeto INT NOT NULL,

    FOREIGN KEY (id_projeto) REFERENCES Projeto(id)
);

-- =========================
-- Tabela associativa: Projeto_planta
-- (Relacionamento N:N "auxilia")
-- =========================
CREATE TABLE Projeto_planta (
    id_projeto INT,
    id_planta INT,

    PRIMARY KEY (id_projeto, id_planta),

    FOREIGN KEY (id_projeto) REFERENCES Projeto(id),
    FOREIGN KEY (id_planta) REFERENCES Planta_cad(id)
);

-- =========================
-- Tabela: Especificacao_Tecnica
-- =========================
CREATE TABLE Especificacao_tecnica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    arquivo VARCHAR(255),
    melhorias TEXT,
    versao INT DEFAULT 1,
    
    id_projeto INT NOT NULL,
    id_antigo INT NULL,

    FOREIGN KEY (id_projeto) REFERENCES Projeto(id),
    FOREIGN KEY (id_antigo) REFERENCES Especificacao_tecnica(id)
);

-- =========================
-- Tabela: Memorial_Calculo
-- =========================
CREATE TABLE Memorial_calculo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    arquivo VARCHAR(255),
    melhorias TEXT,
    versao INT DEFAULT 1,

    id_projeto INT NOT NULL,
    id_antigo INT NULL,

    FOREIGN KEY (id_projeto) REFERENCES Projeto(id),
    FOREIGN KEY (id_antigo) REFERENCES Memorial_calculo(id)
);