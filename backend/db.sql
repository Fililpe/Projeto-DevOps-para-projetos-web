create database sistema_estoque;

CREATE TABLE usuarios (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) CHECK (email ~ '^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$') NOT NULL,
    senha_hash VARCHAR(255) CHECK (length(senha_hash) > 0)
);

CREATE TABLE produtos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    preco NUMERIC(10, 2) NOT NULL CHECK (preco >= 0),
    quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0)
);
