#!/bin/sh

# Aborta o script se algum comando falhar
set -e

# Delay para aguardar o MariaDB subir
echo "Aguardando MariaDB iniciar (10s)..."
sleep 10

echo "Rodando migrações do Alembic..."
alembic upgrade head

echo "Iniciando a aplicação..."
# Executa o comando que foi passado no CMD do Dockerfile
exec "$@"
