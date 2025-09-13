CREATE TABLE produtos (
  produtoid SERIAL PRIMARY KEY,
  nomeproduto VARCHAR(100) NOT NULL,
  categoria VARCHAR(50) NOT NULL,
  preco NUMERIC(10,2) NOT NULL
);

CREATE TABLE vendas (
  vendaid SERIAL PRIMARY KEY,
  nomeproduto VARCHAR(300) NOT NULL,
  quantidade INT NOT NULL,
  datavenda DATE NOT NULL
);