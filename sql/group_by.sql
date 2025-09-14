SELECT
    v.nomeproduto,
    SUM(v.quantidade) AS quantidade_total,
    SUM(v.quantidade * p.preco) AS valor_total_venda
FROM 
    vendas v
JOIN 
    produtos p ON v.nomeproduto = p.nomeproduto
GROUP BY 
    v.nomeproduto
ORDER BY 
    valor_total_venda DESC;