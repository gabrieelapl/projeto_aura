CREATE DATABASE aura_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aura_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

INSERT INTO usuarios (nome, email, senha)
VALUES ('bia', 'teste@aura.com', 
        'abobora'); 