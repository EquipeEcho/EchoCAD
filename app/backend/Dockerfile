FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=builder /app/.venv /app/.venv

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
uv sync --frozen --no-dev

# Garantir que o ambiente virtual do uv seja usado automaticamente
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# 6. Comando para rodar o FastAPI
# Usando o comando padrão do FastAPI (que internamente usa o uvicorn)
CMD ["fastapi", "run", "src/main.py", "--port", "8000"]