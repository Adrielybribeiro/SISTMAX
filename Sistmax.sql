DROP DATABASE IF EXISTS Sistmax;
CREATE DATABASE Sistmax;
USE Sistmax;

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_usuario ENUM('básico + anúncios', 'pro', 'premium') NOT NULL  -- Tipo de usuário ajustado
);

-- Tabela de assinaturas
CREATE TABLE assinaturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    plano ENUM('básico + anúncios', 'pro', 'premium') NOT NULL,  -- Plano ajustado
    data_inicio DATETIME NOT NULL,
    data_fim DATETIME DEFAULT NULL,  -- Permitir NULL se a assinatura for contínua
    status ENUM('ativa', 'inativa', 'cancelada') NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela de conteúdos
CREATE TABLE conteudos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(100),
    ano_lancamento INT(4) NOT NULL,
    tipo ENUM('filme', 'serie') NOT NULL,
    duracao_minutos INT,
    classificacao_indicativa VARCHAR(50)
);

-- Tabela de episódios
CREATE TABLE episodios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo_id INT NOT NULL,
    temporada INT NOT NULL,
    numero_episodio INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    duracao_minutos INT NOT NULL,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
);

-- Histórico de visualizações
CREATE TABLE historico_visualizacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    episodio_id INT DEFAULT NULL,
    data_visualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    tempo_assistido INT NOT NULL,  -- Tempo assistido em minutos
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE,
    FOREIGN KEY (episodio_id) REFERENCES episodios(id) ON DELETE SET NULL  -- Episódio pode ser NULL
);

-- Recomendações
CREATE TABLE recomendacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    motivo TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
);

-- Avaliações dos conteúdos
CREATE TABLE avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    nota FLOAT NOT NULL,  -- Nota da avaliação
    comentario TEXT,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
);

-- Downloads
CREATE TABLE downloads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    episodio_id INT DEFAULT NULL,
    data_download DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiracao DATETIME NOT NULL,  -- Data de expiração do download
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE,
    FOREIGN KEY (episodio_id) REFERENCES episodios(id) ON DELETE SET NULL  -- Episódio pode ser NULL
);

-- Favoritos
CREATE TABLE favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    conteudo_id INT NOT NULL,
    data_adicao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
);
