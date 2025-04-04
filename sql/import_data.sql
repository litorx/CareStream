SET client_encoding TO 'UTF8';

-- Derruba tabelas de staging, se existirem
DROP TABLE IF EXISTS temp_demonstracoes;
DROP TABLE IF EXISTS temp_cadastro;

-- Cria tabela de staging para demonstrações contábeis
CREATE TABLE temp_demonstracoes (
    data_referencia TEXT,
    codigo TEXT,
    registro_ans TEXT,
    descricao TEXT,
    valor1 TEXT,
    valor2 TEXT
);

-- Cria tabela de staging para cadastro de operadoras (assumindo que o CSV possui 5 colunas)
CREATE TABLE temp_cadastro (
    registro_ans TEXT,
    cnpj TEXT,
    razao_social TEXT,
    extra_col TEXT,
    modalidade TEXT
);

-- Importa os CSVs para demonstracoes_contabeis
\copy temp_demonstracoes(data_referencia, codigo, registro_ans, descricao, valor1, valor2) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/1T2023_utf8.csv' CSV DELIMITER ';' HEADER;
\copy temp_demonstracoes(data_referencia, codigo, registro_ans, descricao, valor1, valor2) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/2T2023_utf8.csv' CSV DELIMITER ';' HEADER;
\copy temp_demonstracoes(data_referencia, codigo, registro_ans, descricao, valor1, valor2) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/3T2023_utf8.csv' CSV DELIMITER ';' HEADER;
\copy temp_demonstracoes(data_referencia, codigo, registro_ans, descricao, valor1, valor2) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/4T2023_utf8.csv' CSV DELIMITER ';' HEADER;
\copy temp_demonstracoes(data_referencia, codigo, registro_ans, descricao, valor1, valor2) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/1T2024_utf8.csv' CSV DELIMITER ';' HEADER;
\copy temp_demonstracoes(data_referencia, codigo, registro_ans, descricao, valor1, valor2) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/2T2024_utf8.csv' CSV DELIMITER ';' HEADER;
\copy temp_demonstracoes(data_referencia, codigo, registro_ans, descricao, valor1, valor2) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/3T2024_utf8.csv' CSV DELIMITER ';' HEADER;
\copy temp_demonstracoes(data_referencia, codigo, registro_ans, descricao, valor1, valor2) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/4T2024_utf8.csv' CSV DELIMITER ';' HEADER;

-- Importa o CSV de cadastro de operadoras (5 colunas)
\copy temp_cadastro(registro_ans, cnpj, razao_social, extra_col, modalidade) FROM 'C:/Users/VitorX/OneDrive/Documentos/Projetos/Intuitive Care/data/Relatorio_cadop_utf8.csv' CSV DELIMITER ';' HEADER;

-- Insere dados finais em demonstracoes_contabeis (conversões necessárias)
INSERT INTO demonstracoes_contabeis (data_referencia, codigo, registro_ans, descricao, valor1, valor2)
SELECT 
    CASE 
       WHEN data_referencia ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN TO_DATE(data_referencia, 'YYYY-MM-DD')
       WHEN data_referencia ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$' THEN TO_DATE(data_referencia, 'DD/MM/YYYY')
       ELSE NULL
    END,
    NULLIF(codigo, '')::INTEGER,
    NULLIF(registro_ans, '')::INTEGER,
    descricao,
    REPLACE(valor1, ',', '.')::NUMERIC,
    REPLACE(valor2, ',', '.')::NUMERIC
FROM temp_demonstracoes;

-- Insere dados finais em cadastro_operadoras (selecionando campos relevantes)
INSERT INTO cadastro_operadoras (registro_ans, razao_social, cnpj, modalidade)
SELECT registro_ans, razao_social, cnpj, modalidade
FROM temp_cadastro;

-- Remove tabelas de staging
DROP TABLE temp_demonstracoes;
DROP TABLE temp_cadastro;

SET client_encoding TO 'UTF8';
