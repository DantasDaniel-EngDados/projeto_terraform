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