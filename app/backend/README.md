# EchoCAD API - Backend

API FastAPI para desenvolvimento e testes de upload e processamento de plantas CAD.

## Objetivo

Este README descreve como executar o backend localmente (modo desenvolvimento) e via Docker Compose (Produção).

## Conteúdo

- Pré-requisitos
- Configurar o ambiente (.env)
- Executar localmente (venv ou `uv`/`uv run`)
- Executar com Docker Compose (inclui perfis opcionais)
- Migrações (Alembic)

## Pré-requisitos

- Python 3.13+ (ou 3.10+ compatível com dependências)
- Docker
- opcional: `pipx` para instalar `uv` globalmente (recomendado para fluxo `uv sync`)

Verifique:

```bash
python --version
docker --version
docker compose version
```

## Configurar ambiente

1. Copie o modelo de ambiente e ajuste valores sensíveis:

```bash
cp .env.example .env
# Edite .env com seus valores locais (DB, JWT, chaves, etc.)
```

2. Para desenvolvimento local, normalmente deixe as URLs apontando para `localhost` (veja `.env.example`). Para execução via Docker Compose, o host do banco usado internamente é `mariadb` (nome do serviço).

Principais variáveis em `.env`:

- `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_ROOT_PASSWORD`
- `DATABASE_URL`, `DATABASE_ASYNC_URL` (são usadas pela aplicação e por Alembic)
- `API_PORT` (porta do backend em host quando rodando via Docker)

> Observação: o arquivo `.env.example` contém valores de exemplo para facilitar testes. Não comite seu `.env` com segredos.

## Executar localmente (recomendado para desenvolvimento)

Opção A — com `python -m venv` (sem `pipx`):

```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
# Aplicar migrações localmente (requer que DATABASE_URL aponte para um DB acessível)
alembic upgrade head
# Iniciar a API (usa uvicorn via fastapi/uvicorn)
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Opção B — com `uv` (fluxo usado no Dockerfile, via `pipx`):

```bash
# instalar pipx se necessário
python3 -m pip install --user pipx && python3 -m pipx ensurepath
pipx install uv

cd app/backend
# sincronizar ambiente (instala dependências no virtualenv local conforme pyproject)
uv sync
# rodar a aplicação
uv run fastapi run src/main.py --host 127.0.0.1 --port 8000 --reload
```

Depois disso, a API ficará disponível em `http://127.0.0.1:8000`.

Para testar um upload (exemplo com `httpie`):

```bash
pipx install httpie
http --form POST http://127.0.0.1:8000/upload file@/caminho/arquivo.dwg
```

## Executar com Docker Compose

O compose principal em `app/docker-compose.yaml` orquestra MariaDB, backend, frontend e serviços opcionais (como `cloudflared` e `ollama`) via perfis.

Subir todo o stack padrão (sem perfis opcionais):

```bash
cd app
docker compose up -d --build
```

Subir com perfis opcionais (ex.: `ollama` e `cloudflared`):

```bash
docker compose --profile ollama --profile cloudflared up -d --build
```

Observações:

- O serviço `backend` executa `start.sh` como `ENTRYPOINT`. Esse script aguarda o banco e aplica `alembic upgrade head` automaticamente antes de iniciar a aplicação.
- Se quiser aplicar migrações manualmente via container:

```bash
docker compose exec backend alembic upgrade head
```

## Migrações (Alembic)

As migrações são controladas por Alembic (`alembic/versions`). O `start.sh` já roda `alembic upgrade head` no container.

Para rodar as migrações localmente, garanta que `DATABASE_URL` esteja correto no seu `.env` e execute:

```bash
alembic upgrade head
```

## Notas adicionais

- O `Dockerfile` usa `uv sync` durante o build para instalar dependências conforme `pyproject.toml`. Isso espelha o fluxo recomendado com `uv`/`pipx` para desenvolvimento.
- Serviços opcionais no compose:
	- `cloudflared` está configurado com profile `cloudflared` (executar com `--profile cloudflared` para habilitar).
	- `ollama` e `ollama-model-puller` foram adicionados sob o profile `ollama` (use `--profile ollama`).
