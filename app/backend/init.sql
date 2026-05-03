-- Script de inicialização do banco echocad_db
-- Apenas cria o banco. As tabelas serão criadas automaticamente pelo Alembic.

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- A configuração do MySQL acontece via environment variables:
-- MYSQL_DATABASE: echocad_db (criado automaticamente)
-- MYSQL_USER: echocad_admin
-- MYSQL_PASSWORD: echocad_admin_password

-- Informações finais
SELECT "✓ Banco echocad_db criado com sucesso" as Status;
SELECT "✓ Tabelas serão criadas automaticamente pelo Alembic" as ProximosPasso;

