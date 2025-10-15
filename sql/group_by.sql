INSERT INTO vendaspormes (nomeproduto, quantidade_total, valor_total_venda, mes_venda, ano_venda)
SELECT
    v.nomeproduto,
    SUM(v.quantidade) AS quantidade_total,
    SUM(v.quantidade * p.preco) AS valor_total_venda,
    DATE_TRUNC('month', v.datavenda) AS mes_venda,
    DATE_TRUNC('year', v.datavenda) AS ano_venda
FROM 
    vendas v
JOIN 
    produtos p ON v.nomeproduto = p.nomeproduto
GROUP BY 
    v.nomeproduto,
    mes_venda,
    ano_venda
ON CONFLICT (nomeproduto, mes_venda, ano_venda) DO UPDATE
SET
    quantidade_total = vendaspormes.quantidade_total + EXCLUDED.quantidade_total,
    valor_total_venda = vendaspormes.valor_total_venda + EXCLUDED.valor_total_venda;
