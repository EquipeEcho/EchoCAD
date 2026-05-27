FROM python:3.13-slim AS builder

# Instalar uv para o build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# Instalar dependências usando cache do uv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
# --no-dev

# Estágio Final: Runtime
FROM python:3.13-slim AS runtime

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

# Copiar apenas o ambiente virtual (não precisamos do uv aqui)
COPY --from=builder /app/.venv /app/.venv

# Copiar apenas o necessário
COPY src ./src
# Se houver outros arquivos essenciais na raiz (como alembic.ini), adicione-os aqui:
COPY alembic.ini .
COPY alembic ./alembic
COPY start.sh .
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

EXPOSE 8000

ENTRYPOINT ["./start.sh"]

# Comando para rodar o FastAPI
CMD ["fastapi", "run", "src/main.py", "--port", "8000"]