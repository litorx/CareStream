-- Query 1: Top 10 operadoras (identificadas por registro_ans) com maiores despesas no último trimestre (2024-04-01 a 2024-06-30)
SELECT 
    registro_ans AS operadora,
    valor2 AS despesa_medico_hospitalar
FROM demonstracoes_contabeis
WHERE data_referencia BETWEEN '2024-04-01' AND '2024-06-30'
  AND lower(descricao) LIKE '%eventos%'
  AND lower(descricao) LIKE '%sinistros%'
ORDER BY valor2 DESC
LIMIT 10;

-- Query 2: Top 10 operadoras com maiores despesas nessa categoria no último ano (2024)
SELECT 
    registro_ans AS operadora,
    SUM(valor2) AS total_despesas_ano
FROM demonstracoes_contabeis
WHERE data_referencia BETWEEN '2024-01-01' AND '2024-12-31'
  AND lower(descricao) LIKE '%eventos%'
  AND lower(descricao) LIKE '%sinistros%'
GROUP BY registro_ans
ORDER BY total_despesas_ano DESC
LIMIT 10;