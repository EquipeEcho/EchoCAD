CREATE DATABASE EchoCAD_SQL;
USE EchoCAD_SQL;

-- mapeado em orm (wesley) - last updated 26.03.2026
CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- mapeado em orm (Wesley)
CREATE TABLE Projetos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    descricao_projeto TEXT,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);

CREATE TABLE Comandos_ia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comando_original TEXT,
    intencao_detectada VARCHAR(255),
    parametros_extraidos JSON,
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT,
    id_projetos INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id),
    FOREIGN KEY (id_projetos) REFERENCES Projetos(id)
);

CREATE TABLE Documentos_gerados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(100),
    caminho_arquivo VARCHAR(255),
    data_geracao DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Especificacoes_tecnicas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_documentos_gerados INT,
    categoria_tecnica VARCHAR(100),
    descricao TEXT,
    materiais_previstos TEXT,
    norma_referencia VARCHAR(150),
    observacoes TEXT,
    FOREIGN KEY (id_documentos_gerados) REFERENCES Documentos_gerados(id)
);

CREATE TABLE Calculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100),
    entrada_json JSON,
    resultado_json JSON,
    regra_aplicada TEXT
);

CREATE TABLE Memoriais_calculo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_documentos_gerados INT,
    id_calculos INT,
    resultados TEXT,
    norma_referencia VARCHAR(150),
    observacoes TEXT,
    FOREIGN KEY (id_documentos_gerados) REFERENCES Documentos_gerados(id),
    FOREIGN KEY (id_calculos) REFERENCES Calculos(id)
);

CREATE TABLE Elementos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    layer VARCHAR(100),
    geometria VARCHAR(100),
    comprimento DECIMAL(10,2),
    area DECIMAL(10,2),
    categoria_tecnica_tipo VARCHAR(100)
);

CREATE TABLE Arquivos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    caminho VARCHAR(255),
    nome_arquivo VARCHAR(150),
    tipo VARCHAR(50),
    id_projetos INT,
    id_calculos INT,
    id_documentos_gerados INT,
    id_elementos INT,
    FOREIGN KEY (id_projetos) REFERENCES Projetos(id),
    FOREIGN KEY (id_calculos) REFERENCES Calculos(id),
    FOREIGN KEY (id_documentos_gerados) REFERENCES Documentos_gerados(id),
    FOREIGN KEY (id_elementos) REFERENCES Elementos(id)
);

CREATE TABLE Coordenadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_elementos INT,
    x DECIMAL(10,4),
    y DECIMAL(10,4),
    ordem INT,
    FOREIGN KEY (id_elementos) REFERENCES Elementos(id)
);

CREATE TABLE Processamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(50),
    data_inicio DATETIME,
    data_fim DATETIME,
    log_erro TEXT,
    versao_parser VARCHAR(50),
    id_arquivos INT,
    FOREIGN KEY (id_arquivos) REFERENCES Arquivos(id)
); 

INSERT INTO Usuario (nome, email, senha)
VALUES ('admin', 'admin@echocad.com', 'admin123');