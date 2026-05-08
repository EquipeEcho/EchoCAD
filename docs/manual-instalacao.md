# 📖 Manual de Instalação - EchoCAD

## 📋 Sumário

- [Pré-requisitos](#requisitos)
- [Instalação do Ambiente](#instalacao-ambiente)
- [Configuração do Banco de Dados](#config-banco-dados)
- [Instalação das Dependências](#instalacao-dependencias)
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

## 2. Acesse a pasta principal da aplicação

```bash
cd app
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

Lembre-se de atualizar as informações dos arquivos presentes no backend com os dados do usuário do seu MySQL

## Atualizando o banco de dados

Dentro da pasta backend/src instale o alembic com os seguintes comandos:

```bash
# Instala o alembic
pip install alembic

# Atualiza as tabelas do banco de dados
alembic upgrade head
```

---

# <span id="instalacao-dependencias">Instalação das Dependências</span>

## Frontend

Navegue até a pasta do frontend com o seguinte comando:

```bash
cd frontend
```

Para instalar as dependências utilize o comando:
```bash
npm install
```

> Não feche o terminal ainda, você terá que abrir dois deles para rodar completamente o projeto

## Backend

Abra outro terminal para executar as seguintes funções, caso esteja usando o CMD você terá que abrir outro, mas com o VS Code basta clicar no sinal de `+` na direita no botão `TERMINAL` e `PORTS`.

A partir da pasta `app` navegue até a pasta do backend

```bash
cd backend
```

Instale as dependências com o comando:
```bash
pip install uv

# Verifica a instalação do uv
uv --version

# Instala as dependências do projeto
uv sync
```

Antes de rodar o "uv sync", garanta que está na mesma pasta do arquivo **pyproject.toml**

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
uv run main.py
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
