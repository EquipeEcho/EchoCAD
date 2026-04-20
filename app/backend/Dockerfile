FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copia o código fonte
COPY . .

EXPOSE 8000

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Garantir que o ambiente virtual do uv seja usado automaticamente
ENV PATH="/app/.venv/bin:$PATH"

# 6. Comando para rodar o FastAPI
# Usando o comando padrão do FastAPI (que internamente usa o uvicorn)
CMD ["fastapi", "run", "main.py", "--port", "8000"]