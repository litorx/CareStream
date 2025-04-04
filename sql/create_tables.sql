DROP TABLE IF EXISTS demonstracoes_contabeis;
DROP TABLE IF EXISTS cadastro_operadoras;

CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    data_referencia DATE NOT NULL,
    codigo INTEGER,
    registro_ans INTEGER,
    descricao TEXT,
    valor1 NUMERIC(15,2),
    valor2 NUMERIC(15,2),
    data_insercao TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cadastro_operadoras (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(50),
    razao_social VARCHAR(255),
    cnpj VARCHAR(20),
    modalidade VARCHAR(50),
    data_insercao TIMESTAMP DEFAULT NOW()
);
