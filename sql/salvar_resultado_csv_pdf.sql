SELECT
    nomeproduto,
    quantidade_total,
    valor_total_venda,
    EXTRACT(MONTH FROM mes_venda) AS mes_venda,
    EXTRACT(YEAR FROM ano_venda) AS ano_venda
FROM vendaspormes
ORDER BY ano_venda, mes_venda, valor_total_venda DESC;