CREATE DATABASE aura_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aura_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

ALTER TABLE usuarios ADD COLUMN bio TEXT;

INSERT INTO usuarios (nome, email, senha, bio)
VALUES ('Maria Silva', 'maria.silva@gmail.com', 'senha123', 'Pesquisadora e estudante de IA...');

-- Adiciona coluna 'membro_desde' com data/hora de criação
ALTER TABLE usuarios 
ADD COLUMN membro_desde DATETIME DEFAULT CURRENT_TIMESTAMP;

UPDATE usuarios SET senha = SHA2(senha, 256);