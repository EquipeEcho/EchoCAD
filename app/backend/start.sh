#!/bin/sh

# Aborta o script se algum comando falhar
set -e

echo "Rodando migrações do Alembic..."
alembic upgrade head

echo "Iniciando a aplicação..."
# Executa o comando que foi passado no CMD do Dockerfile
exec "$@"
