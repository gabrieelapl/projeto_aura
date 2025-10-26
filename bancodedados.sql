-- ======================================
-- 1. Criar Banco de Dados
-- ======================================
CREATE DATABASE IF NOT EXISTS aura_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE aura_db;

-- ======================================
-- 2. Tabelas
-- ======================================

-- 2.1 Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    bio TEXT,
    membro_desde DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2.2 Artigos
CREATE TABLE IF NOT EXISTS artigos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    resumo TEXT,
    palavras_chave TEXT, -- ex: "PLN,Revisão Sistemática,Educação,ODS"
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2.3 Selecionar Resumo
CREATE TABLE IF NOT EXISTS selecionar_resumo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resumo TEXT NOT NULL,
    palavras_chave TEXT,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2.4 Perguntas
CREATE TABLE IF NOT EXISTS perguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artigo_id INT NOT NULL,
    pergunta TEXT NOT NULL,
    alternativa_a TEXT NOT NULL,
    alternativa_b TEXT NOT NULL,
    alternativa_c TEXT NOT NULL,
    alternativa_d TEXT NOT NULL,
    resposta_correta CHAR(1) NOT NULL,  -- 'A', 'B', 'C', 'D'
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artigo_id) REFERENCES artigos(id)
);

-- 2.5 Tópicos Principais
CREATE TABLE IF NOT EXISTS topicos_principais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artigo_id INT NOT NULL,
    topico TEXT NOT NULL,
    FOREIGN KEY (artigo_id) REFERENCES artigos(id)
);

-- 2.6 Citações
CREATE TABLE IF NOT EXISTS citacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artigo_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    autores VARCHAR(255) NOT NULL,
    citado INT DEFAULT 0,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artigo_id) REFERENCES artigos(id)
);

-- ======================================
-- 3. Inserções
-- ======================================

-- 3.1 Usuários
INSERT INTO usuarios (nome, email, senha, bio)
VALUES ('Maria Silva', 'maria.silva@gmail.com', 'senha123', 'Pesquisadora e estudante de IA...');

-- 3.2 Artigos
INSERT INTO artigos (titulo, resumo, palavras_chave)
VALUES (
    'IA no Ensino Superior - Exemplo',
    'O artigo aborda como a Inteligência Artificial (IA) está transformando o ensino superior, personalizando o aprendizado, identificando dificuldades, reduzindo custos e tornando as aulas mais dinâmicas. Apesar dos benefícios, a IA apresenta desafios como ética, dependência tecnológica e a necessidade de capacitação docente. A IA consiste em sistemas capazes de realizar tarefas típicas da inteligência humana e, no ensino superior, é aplicada em tutoria inteligente, análise de dados e recomendações de conteúdo, possibilitando experiências de aprendizagem mais personalizadas e eficazes. Entre as aplicações práticas estão tutoria inteligente, análise preditiva para identificar alunos com dificuldades, chatbots educacionais para dúvidas frequentes, correção automática de avaliações e adaptação de conteúdos conforme o perfil do estudante. Os principais desafios incluem ética e privacidade, desigualdade de acesso, capacitação docente e dependência tecnológica.',
    'PLN,Revisão Sistemática,Educação,ODS'
);

-- 3.3 Perguntas
INSERT INTO perguntas (artigo_id, pergunta, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta)
VALUES 
(1, 'Qual é a principal contribuição deste artigo de pesquisa?',
 'A principal contribuição é um algoritmo que reduz o tempo de treinamento de redes neurais profundas sem comprometer a performance do modelo de transformador em domínios especializados.',
 'A proposta contribui com uma metodologia para melhorar a robustez de sistemas de recomendação baseados em preferências do usuário.',
 'O estudo descreve um novo paradigma para integrar dados não estruturados em modelos preditivos de aprendizado de máquina.',
 'O artigo oferece uma abordagem para melhorar a precisão de modelos de classificação em tarefas de reconhecimento de voz.',
 'B'),
(1, 'Como os resultados deste estudo impactam a área de conhecimento?',
 'O estudo propõe um novo algoritmo de clustering adaptativo para melhorar a segmentação de grandes volumes de dados do modelo de transformador em domínios especializados.',
 'A contribuição deste trabalho é uma abordagem novel de pré-processamento de dados para redes neurais em tarefas de visão computacional.',
 'O artigo apresenta uma estratégia para melhorar a interpretação e a explicabilidade de modelos de aprendizado profundo.',
 'A pesquisa oferece uma solução para otimizar o uso de recursos computacionais em tarefas de aprendizado supervisionado.',
 'C'),
(1, 'Quais limitações o autor aponta em sua pesquisa?',
 'A contribuição central é uma técnica para reduzir o viés em algoritmos de aprendizado automático aplicados em dados sensíveis.',
 'O artigo propõe uma abordagem de otimização que melhora a precisão e a eficiência de modelos de tradução automática.',
 'A principal inovação é o desenvolvimento de uma rede neural mais robusta para processamento de linguagem natural em contextos diversos.',
 'A pesquisa introduz um novo método de regularização em redes neurais que aumenta a generalização do modelo.',
 'D'),
(1, 'Quais metodologias foram usadas para coleta e análise dos dados?',
 'O artigo oferece uma solução eficiente para melhorar a detecção de anomalias em grandes conjuntos de dados financeiros do modelo de transformador em domínios especializados.',
 'A principal inovação é a introdução de um método híbrido que combina aprendizado supervisionado e não supervisionado.',
 'A pesquisa apresenta um novo framework que melhora a escalabilidade de sistemas de recomendação baseados em aprendizado de máquina.',
 'O estudo descreve um modelo de rede neural capaz de prever tendências de mercado com base em dados históricos.',
 'B'),
(1, 'Como os achados podem ser aplicados na prática profissional?',
 'A principal contribuição é um mecanismo de atenção modificado que melhora o desempenho do modelo de transformador em domínios especializados.',
 'A proposta contribui com uma nova abordagem para aumentar a precisão na classificação de grandes volumes de dados em tempo real.',
 'Este estudo apresenta um algoritmo inovador que otimiza o desempenho de redes neurais convolucionais em tarefas de reconhecimento de imagem.',
 'A pesquisa propõe uma técnica avançada de aprendizado profundo, reduzindo a complexidade computacional em modelos preditivos.',
 'D');

-- 3.4 Tópicos Principais
INSERT INTO topicos_principais (artigo_id, topico) VALUES
(1, 'Introduz um mecanismo de atenção modificado'),
(1, 'Demonstra uma melhoria de 15% em relação aos métodos SOTA'),
(1, 'Fornece um procedimento de treinamento mais eficiente'),
(1, 'Apresenta desempenho robusto em vários idiomas'),
(1, 'Inclui estudos extensivos de ablação');

-- 3.5 Citações
INSERT INTO citacoes (artigo_id, titulo, autores, citado) VALUES
(1, 'Classificação de Imagens com Redes Neurais Convolucionais Profundas', 'Krizhevsky, Sutskever e Hinton (2012)', 4),
(1, 'BERT: Pré-treinamento de Representações Profundas de Linguagem', 'Devlin et al. (2018)', 3),
(1, 'Redes Residuais Profundas para Reconhecimento de Imagens', 'He et al. (2016)', 2),
(1, 'Transformers: Uma Abordagem Geral para Modelagem de Sequência', 'Wolf et al. (2020)', 2),
(1, 'GPT-3: Modelos de Linguagem São Aprendizes de Poucos Exemplos', 'Brown et al. (2020)', 1),
(1, 'T5: Explorar a Transferência de Texto para Texto com um Modelo Unificado', 'Raffel et al. (2020)', 1),
(1, 'XLNet: Superando o BERT com Modelagem Autoregressiva Generalizada', 'Yang et al. (2019)', 1),
(1, 'Word2Vec: Eficiência de Vetores de Palavras de Grande Dimensão', 'Mikolov et al. (2013)', 1),
(1, 'Atenção é Tudo que Você Precisa', 'Vaswani et al. (2017)', 5),
(1, 'Classificação de Imagens com Redes Neurais Convolucionais Profundas', 'Krizhevsky, Sutskever e Hinton (2012)', 4);

-- ======================================
-- 4. Ajuste de Foreign Keys (sem ON DELETE CASCADE)
-- ======================================
ALTER TABLE perguntas
DROP FOREIGN KEY IF EXISTS perguntas_ibfk_1;

ALTER TABLE perguntas
ADD CONSTRAINT perguntas_ibfk_1
FOREIGN KEY (artigo_id) REFERENCES artigos(id);

ALTER TABLE citacoes
DROP FOREIGN KEY IF EXISTS citacoes_ibfk_1;

ALTER TABLE citacoes
ADD CONSTRAINT citacoes_ibfk_1
FOREIGN KEY (artigo_id) REFERENCES artigos(id);