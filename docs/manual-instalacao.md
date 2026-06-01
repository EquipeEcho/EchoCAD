# 📖 Manual de Instalação - EchoCAD

## 📋 Sumário

- [Pré-requisitos](#requisitos)
- [Instalação do Ambiente](#instalacao-ambiente)
- [Instalação das Dependências](#instalacao-dependencias)
- [Configuração do Banco de Dados](#config-banco-dados)
- [Execução do Projeto](#execucao-projeto)
- [Solução de Problemas](#solucao-problemas)

---

## 🔧 <span id="requisitos">Pré-requisitos</span>

Antes de iniciar a instalação, certifique-se de ter os seguintes softwares instalados em seu sistema:

### Obrigatórios

- **Armazenamento**
    - Verifique se possui 300MB disponíveis para fazer a instalação do projeto
    - Além do espaço adicional para armazenar as informações no banco de dados

- **Node.js** (versão 18.x ou superior)
  - Download: https://nodejs.org/
  - Verifique a instalação: `node --version`

- **pnpm** (gerenciador de pacotes)
  - Instalação: `npm install -g pnpm`
  - Verifique a instalação: `pnpm --version`

- **Git**
  - Download: https://git-scm.com/downloads
  - Verifique a instalação: `git --version`

- **Python**
  - Download: https://www.python.org/downloads/
  - Verifique a instalação: `python --version`

- **MySQL Workbench**
  - Download: https://dev.mysql.com/downloads/workbench/


### Opcionais (mas recomendados)

- **VS Code** (Editor de código)
  - Download: https://code.visualstudio.com/
 
- **Docker** (Alternativa para o MySQL Workbench)
  - Download: https://docs.docker.com/desktop/setup/install/windows-install/

---


# 🚀 <span id="instalacao-ambiente">Instalação do Ambiente</span>

## 1. Clone o Repositório

Abra o prompt de comando (cmd) e navegue até a pasta em que deseja armazenar o projeto.

```bash
# utilize o comando "cd" + nome da pasta
cd nome_pasta

# Clona o projeto na pasta atual
git clone https://github.com/EquipeEcho/EchoCAD
```

---

# <span id="instalacao-dependencias">Instalação das Dependências</span>

## Frontend

Navegue até a pasta do frontend com o seguinte comando:

```bash
cd app/frontend
```

Para instalar as dependências utilize o comando:
```bash
npm install
```

> Não feche o terminal ainda, você terá que abrir dois deles para rodar completamente o projeto

## Backend

Abra outro terminal para executar as seguintes funções, caso esteja usando o CMD você terá que abrir outro, mas com o VS Code basta clicar no sinal de `+` na direita no botão `TERMINAL` e `PORTS`.

A partir da pasta `EchoCAD` navegue até a pasta do backend

```bash
cd app/backend
```

Faça a instalação do pipx para isolar os aplicativos Python

```bash
pip install pipx
```

Instale as dependências com o comando:
```bash
# Instala o uv
pipx install uv

# Verifica a instalação do uv
uv --version

# Instala as dependências do projeto
uv sync
```

---

# 🗄️ <span id="config-banco-dados">Configuração do Banco de Dados</span>

## Configurações utilizando o MySQL Workbench

Caso ainda não tenha nenhuma connection criada (indicada por uma caixa abaixo do texto `MySQL Connections`) siga as seguintes instruções para criar uma.

- Pesquise por `serviços` na barra de pesquisa
- Procure por `MySQL80` na lista de serviços e execute-o caso não esteja "Em execução" clicando com o botão direito e depois em `iniciar`
- Voltando para o MySQL Workbench, clique no ícone de `+` no lado direito do texto `MySQL Connections`
- Preencha o primeiro campo com o nome da conexão (você pode inserir qualquer nome que desejar)
- Teste a conexão com o botão `Test Connection` para garantir que está funcionando
- Clique em OK para criar uma conexão.

## Criando o banco de dados no MySQL

No query exibido basta executar o seguinte comando para criar um banco de dados
```bash
create database echocad_db;
```

Lembre-se de atualizar as informações dos arquivos presentes no backend com os dados do usuário do seu MySQL.
Os arquivos que deve modificar são esses:
- EchoCAD/app/backend/src/config.py - Linha 5
- EchoCAD/app/backend/alembic.ini - Linha 89

Na parte onde está **echocad_admin:echocad_admin_password** mude para o nome:sua_senha

## Atualizando o banco de dados

Considerando que, no terminal, está dentro da pasta EchoCAD:

```bash
# Atualiza as tabelas do banco de dados
alembic upgrade head
```

---

# <span id="execucao-projeto">Execução do projeto</span>

## Frontend

Primeiramente navegue até a pasta destinada para o frontend, caso esteja na pasta `app` digite o seguinte código:

```bash
# Na pasta app
cd frontend
```

Para executar o frontend, utilize o seguinte comando:
```bash
npm run dev
```

O retorno será principalmente uma lista com três links, apenas segure o `Ctrl` e clique no primeiro, ou seja, o Local.

## Backend

Navegue até a pasta backend/src e execute este código

```bash
uv run uvicorn src.main:app --reload
```

## Docker

Utilizar o Docker para deploy em servidor é a forma recomendada. Basta ter o Docker instalado e devidamente funcional — sem necessidade de instalar Python, Node.js ou banco de dados separadamente.

### 1. Clone o repositório

```bash
git clone https://github.com/EquipeEcho/EchoCAD
cd EchoCAD
```

### 2. Configure o arquivo `.env`

Navegue até a pasta `app` e crie o arquivo `.env` a partir do exemplo:

```bash
cd app
cp .env.example .env
```

Edite o `.env` e ajuste os valores obrigatórios:

| Variável | Descrição | Exemplo |
|---|---|---|
| `MYSQL_ROOT_PASSWORD` | Senha do root do banco de dados | `minha_senha_root` |
| `MYSQL_USER` | Usuário do banco de dados | `echocad` |
| `MYSQL_PASSWORD` | Senha do usuário do banco | `echocad_password` |
| `JWT_TOKEN` | Chave secreta para autenticação JWT (use uma string longa e aleatória) | `troque_por_algo_seguro` |
| `GROQ_API_KEY` | Chave da API Groq para geração de especificações com IA | `gsk_...` |
| `DATABASE_URL` | URL de conexão síncrona — mantenha `mariadb` como host no Docker | `mysql+pymysql://echocad:echocad_password@mariadb:3306/echocad_db` |
| `DATABASE_ASYNC_URL` | URL de conexão assíncrona — mesmo host `mariadb` | `mysql+aiomysql://echocad:echocad_password@mariadb:3306/echocad_db` |

> **Atenção:** As URLs do banco de dados usam `mariadb` como hostname (nome do serviço Docker). Não troque por `localhost`.

### 3. Suba os containers

#### Opção A — Somente o sistema principal (sem IA local)

Sobe 3 containers: banco de dados (MariaDB), backend (FastAPI) e frontend (Nginx).
A geração de especificações técnicas usará a API Groq — configure `GROQ_API_KEY` no `.env`.

```bash
docker compose up -d --build
```

#### Opção B — Com Ollama (IA local, sem depender da Groq)

Sobe 5 containers: os 3 acima + Ollama (servidor de IA) + um puller que baixa automaticamente o modelo `qwen2.5:7b`.

> **Atenção:** O modelo ocupa aproximadamente **5 GB** de armazenamento e pode levar alguns minutos para ser baixado na primeira inicialização.

```bash
docker compose --profile ollama up -d --build
```

#### Opção C — Com domínio via Cloudflare Tunnel

Para expor o sistema em um domínio registrado no Cloudflare, adicione o token do túnel no `.env`:

```bash
# No .env
CLOUDFLARED_TOKEN=seu_token_do_cloudflare
```

Depois suba com o perfil `cloudflared`:

```bash
docker compose --profile cloudflared up -d --build
```

#### Opção D — Todos os serviços juntos

```bash
docker compose --profile ollama --profile cloudflared up -d --build
```

Este comando sobe 6 containers: MariaDB, backend, frontend, Ollama, puller de modelo e o túnel Cloudflare.

### 4. Acesse o sistema

Após os containers subirem, acesse pelo navegador:

- **Frontend:** `http://localhost` (porta 80 por padrão, ajustável via `FRONTEND_PORT` no `.env`)
- **API backend:** `http://localhost:8001` (porta ajustável via `API_PORT` no `.env`)

### 5. Acompanhe os logs

```bash
# Todos os serviços
docker compose logs -f

# Apenas o backend
docker compose logs -f backend

# Apenas o banco de dados
docker compose logs -f mariadb
```

### 6. Parar os containers

```bash
docker compose down
```

Para parar **e remover os volumes** (apaga o banco de dados):

```bash
docker compose down -v
```

---

# 🔧 <span id="solucao-problemas">Solução de Problemas</span>

## ❌ Erro: "Module not found"

**Solução:**
```bash
# Limpe o cache e reinstale as dependências
rm -rf node_modules
rm pnpm-lock.yaml
pnpm install
```

## ❌ Erro: "Port 3000 is already in use"

**Solução:**
```bash
# Windows - Encontre e mate o processo na porta 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Ou execute em outra porta
PORT=3001 pnpm dev
```

---

# 📞 Suporte

Se você encontrar problemas durante a instalação:

1. Verifique os logs de erro no terminal
2. Consulte a [documentação oficial do Next.js](https://nextjs.org/docs)
3. Verifique as issues no GitHub do projeto
4. Entre em contato com a equipe de desenvolvimento

---

## 🎉 Instalação Concluída!

Se você chegou até aqui e todos os testes passaram, parabéns! 🚀

Seu ambiente está configurado e pronto para desenvolvimento.

Próximos passos:
- Leia o [Manual do Usuário](https://docs.google.com/document/d/1ekIfzlc30ju7d_bATAOY1NgEiKclbtIQ1lRkMwI_T3M/edit?usp=sharing)
- Explore o código e contribua!

---

**Desenvolvido pela Equipe Echo - FATEC SJC 2026-1**
