# EchoCAD API - Backend

API FastAPI para gerenciar upload e armazenamento de arquivos CAD (.dwg, .dwf, .pdf).

## Tabela de Conteúdos

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
  - [1. Instalar pipx](#1-instalar-pipx)
  - [2. Instalar Poetry](#2-instalar-poetry)
  - [3. Instalar Dependências](#3-instalar-dependências)
- [Executar o Projeto](#executar-o-projeto)
- [Docker](#docker)
  - [Construir a Imagem Docker](#construir-a-imagem-docker)
  - [Executar Container Docker](#executar-container-docker)

---

## Pré-requisitos

Certifique-se de que você tem instalado:
- **Python 3.13+** ([Download aqui](https://www.python.org/downloads/))
- **pip** (geralmente vem com Python)
- **Docker** (opcional, apenas para containerização) ([Download aqui](https://www.docker.com/products/docker-desktop))

Verifique as versões instaladas:
```bash
python --version
pip --version
docker --version  # opcional
```

---

## Instalação

### 1. Instalar pipx

`pipx` é um instalador de ferramentas Python que isola dependências. É a forma recomendada para instalar `Poetry`.

**No Linux/macOS:**
```bash
pip install --upgrade pip
pip install pipx
export PATH="$HOME/.local/bin:$PATH"
```

**No Windows:**
```bash
pip install --upgrade pip
pip install pipx
```

Verifique a instalação:
```bash
pipx --version
```

### 2. Instalar Poetry

`Poetry` é um gerenciador de dependências e empacotador para Python.

```bash
pipx install poetry
poetry --version
```

Caso o comando poetry não seja encontrado após a instalação, adicione o caminho ao PATH:

**Linux/macOS:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Adicione a linha acima ao seu arquivo `~/.bashrc` ou `~/.zshrc` para persistir entre sessões.

### 3. Instalar Dependências

Clone ou navegue até a pasta do projeto e instale as dependências especificadas no `pyproject.toml`:

```bash
cd /caminho/para/EchoCAD/app/backend
poetry install
```

Este comando:
- Cria um ambiente virtual automático
- Instala todas as dependências do projeto
- Sincroniza com o arquivo `poetry.lock`

Para atualizar as dependências:
```bash
poetry self add poetry-plugin-export
```

---

## Executar o Projeto

### Modo Desenvolvimento

Execute a aplicação FastAPI com auto-recarregamento:

```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

### Modo Produção

```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Dentro do Ambiente Virtual

Se preferir entrar no ambiente virtual do Poetry:

```bash
poetry shell
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Para sair do ambiente virtual:
```bash
exit
```

### Testar a API

Fazer upload de arquivo:
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@caminho/do/arquivo.dwg"
```

Acessar documentação Swagger:
```bash
# Abra no navegador:
http://localhost:8000/docs
```

---

## Docker

### Construir a Imagem Docker

Na pasta do projeto, execute:

```bash
docker build -t echocad-api:latest .
```

Verifique se a imagem foi criada:
```bash
docker images | grep echocad-api
```

### Executar Container Docker

**Modo interativo (para desenvolvimento):**
```bash
docker run -it -p 8000:8000 echocad-api:latest
```

**Modo background (para produção):**
```bash
docker run -d \
  --name echocad-api \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  echocad-api:latest
```

Onde:
- `-d`: Executa em background
- `--name echocad-api`: Nome do container
- `-p 8000:8000`: Mapeia porta 8000
- `-v $(pwd)/uploads:/app/uploads`: Monta volume para persistir uploads

### Gerenciar Container Docker

**Ver logs:**
```bash
docker logs echocad-api
docker logs echocad-api -f  # follow (tempo real)
```

**Parar container:**
```bash
docker stop echocad-api
```

**Reiniciar container:**
```bash
docker restart echocad-api
```

**Remover container:**
```bash
docker rm echocad-api
```

**Executar comando dentro do container:**
```bash
docker exec -it echocad-api bash
```

### Acessar a API

Após iniciar o container, acesse:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

---

## 🐳 Docker Compose (Recommended)

### Quick Start

Execute o script automatizado:
```bash
chmod +x setup.sh
./setup.sh
```

Ou manualmente:
```bash
docker-compose up -d
```

### Serviços Iniciados

| Serviço | Container | Porta |
|---------|-----------|-------|
| 🗄️ MySQL | echocad_mysql | 3306 |
| 🤖 Ollama | ollama | 11434 |
| 📥 Model Puller | ollama_puller | - |
| 🚀 API | echocad_api | 8000 |

### Credenciais MySQL

- **Host**: localhost (ou `mysql` dentro do Docker)
- **Port**: 3306
- **Database**: echocad_db
- **User**: echocad_admin
- **Password**: echocad_admin_password

### Modelos AI (Auto-Downloaded)

- qwen2.5:7b (principal)
- qwen2.5:3b (agentes)
- qwen2.5:1.5b (rápido)

### Gerenciar Serviços

```bash
# Status de todos os containers
./docker-manage.sh status
# ou
docker-compose ps

# Visualizar logs (todos)
./docker-manage.sh logs

# Visualizar logs específicos
./docker-manage.sh logs-api      # API
./docker-manage.sh logs-mysql    # MySQL
./docker-manage.sh logs-ollama   # Modelos

# Parar tudo
./docker-manage.sh stop
# ou
docker-compose down

# Limpar tudo (remover volumes)
./docker-manage.sh clean
# ou
docker-compose down -v

# Reiniciar
./docker-manage.sh restart
```

### Acessar Serviços

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MySQL**: localhost:3306 (use DBeaver, MySQL Workbench, etc)
- **Ollama**: http://localhost:11434/api/tags

### Arquivos Importantes

- **docker-compose.yaml** - Configuração dos serviços
- **init.sql** - Schema do banco de dados
- **docker-manage.sh** - Script de gerenciamento
- **.env** - Variáveis de ambiente

### Documentação Completa

Para mais detalhes, veja:
- [QUICKSTART.md](./QUICKSTART.md) - Guia rápido
- [DOCKER_SETUP.md](./DOCKER_SETUP.md) - Documentação detalhada

---

## Estrutura do Projeto

```
src/
├── main.py              # Aplicação FastAPI principal
├── database.py          # Configuração SQLite
├── controller/
│   └── file_controller.py
├── models/
│   └── file_cad.py     # Modelo de dados
└── routes/
    └── upload.py       # Rotas de upload
tests/
├── test_main.py        # Testes unitários
uploads/                # Arquivos carregados (gitignored)
├── Dockerfile          # Configuração Docker
├── pyproject.toml      # Dependências do projeto
├── poetry.lock         # Lock file (não editar manualmente)
├── requirements-docker.txt  # Requirements exportado para Docker
└── README.md           # Este arquivo
```

---

## Solução de Problemas

**Erro: `poetry: command not found`**
```bash
# Reconfigure o PATH
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc  # ou ~/.zshrc
```

**Erro: `ModuleNotFoundError`**
```bash
# Reinstale as dependências
poetry install --no-cache
```

**Erro ao conectar ao banco de dados**
```bash
# Verifique se o arquivo database.db foi criado
ls -la database.db
```

**Container não inicia**
```bash
# Verifique os logs
docker logs echocad-api
```

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (opcional):
```bash
DATABASE_URL=sqlite:///database.db
APP_HOST=0.0.0.0
APP_PORT=8000
```