# EchoCAD API - Backend

API FastAPI para teste e desenvolvimento de upload e processamento de plantas CAD.

## Conteúdo

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Executar](#executar)
- [Estrutura principal](#estrutura-principal)
- [Docker Compose](#docker-compose)
- [Arquivos .env](#arquivos-env)

---

## Pré-requisitos

Tenha instalado:
- Python 3.13+
- pip
- Docker

Verifique:
```bash
python --version
pip --version
docker --version
```

---

## Instalação

### 1. Instalar pipx

No Windows:
```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

No Linux/macOS:
```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

Feche e abra o terminal ou execute:
```bash
source ~/.profile
```

Verifique:
```bash
pipx --version
```

### 2. Instalar uv

```bash
pipx install uv
```

Verifique:
```bash
uv --version
```

### 3. Instalar dependências

```bash
cd /caminho/para/EchoCAD/app/backend
uv sync
```

---

## Executar

### Modo FastAPI dev para teste

```bash
uv run fastapi run src/main.py --host 0.0.0.0 --port 8000 --reload
```

A API estará em `http://localhost:8000`.

### Teste com httpie

O `httpie` é muito útil e mais fácil de usar que o `curl`.

```bash
pipx install httpie
```

Teste upload:

```bash
http --form POST http://localhost:8000/upload file@caminho/do/arquivo.dwg
```

---

## Estrutura principal

- `src/routes`
- `src/controller`
- `src/models`
- `src/schemas`
- `alembic`
- `docker-compose.yaml`
- `Dockerfile`

---

## Docker Compose

Docker é uma plataforma que roda aplicativos em containers isolados.
Instale pelo site oficial ou pelo gerenciador de pacotes.

- Site: https://www.docker.com/get-started
- Windows/macOS: Docker Desktop
- Linux: Docker Engine + Docker Compose plugin

Suba o ambiente de teste:
```bash
docker compose up -d
```

Pare os serviços:
```bash
docker compose down
```

Verifique o status:
```bash
docker compose ps
```

O `docker-compose.yaml` orquestra o MySQL e a migração Alembic.

---

## Arquivos .env

Use `.env` para configurar apenas o que é necessário em desenvolvimento.

Principais variáveis:
- `DATABASE_URL`: conexão MySQL
- `DEBUG`: true ou false

Não comite o `.env`. Use `.env.example` como modelo.

Exemplo:
```env
DATABASE_URL=mysql+pymysql://echocad_admin:echocad_admin_password@localhost:3306/echocad_db
DEBUG=true
```
