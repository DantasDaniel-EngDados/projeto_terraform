CREATE TABLE produtos (
  nomeproduto VARCHAR(100) PRIMARY KEY NOT NULL,
  categoria VARCHAR(50) NOT NULL,
  preco NUMERIC(10,2) NOT NULL

);

CREATE TABLE vendas (
  vendaid SERIAL PRIMARY KEY,
  nomeproduto VARCHAR(300) NOT NULL,
  quantidade INT NOT NULL,
  datavenda DATE NOT NULL
);

CREATE TABLE vendaspormes (
 nomeproduto VARCHAR(100) NOT NULL,
 quantidade_total INT NOT NULL,
 valor_total_venda INT NOT NULL,
 mes_venda DATE NOT NULL,
 ano_venda DATE NOT NULL
);

ALTER TABLE vendaspormes DROP CONSTRAINT IF EXISTS produto_mes_e_ano;

ALTER TABLE vendaspormes
ADD CONSTRAINT produto_mes_e_ano UNIQUE (nomeproduto, mes_venda, ano_venda);