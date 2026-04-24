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

## Configurações de Connections no MySQL

Caso ainda não tenha nenhuma connection criada (indicada por uma caixa abaixo do texto `MySQL Connections`) siga as seguintes instruções para criar uma.

- Pesquise por `serviços` na barra de pesquisa
- Procure por `MySQL80` na lista de serviços e execute-o caso não esteja "Em execução" clicando com o botão direito e depois em `iniciar`
- Voltando para o MySQL Workbench, clique no ícone de `+` no lado direito do texto `MySQL Connections`
- Preencha o primeiro campo com o nome da conexão (você pode inserir qualquer nome que desejar)
- Teste a conexão com o botão `Test Connection` para garantir que está funcionando
- Clique em OK para criar uma conexão.

## Criando o banco de dados no MySQL

Utilize o conteúdo no arquivo databaseSQL.sql presente na pasta `EchoCAD/app/database` para criar o modelo do banco de dados.<br>

Para isso, abra o MySQL digitando `mysql` na barra de pesquisas e clique em `MySQL Workbench`. Selecione uma conexão qualquer e cole o texto do `databaseSQL.sql` dentro do campo de texto que apareceu. <br>

Garanta que você já não possui um banco de dados com o nome de `EchoCAD_SQL` para que não ocorra conflitos.<br>

Execute clicando no botão com um ícone de raio acima da primeira linha do texto ao lado direito no ícone para salvar.<br>

---

# <span id="instalacao-dependencias">Instalação das Dependências</span>

Existem duas maneiras de fazer a instalação das dependências, utilize a que achar melhor, mas certifique-se de executar o projeto como está descrito no manual correspondente, não faça a instalação pelo venv e tente rodar pelo pipx, por exemplo.

## venv

É recomendável criar um ambiente virtual, pois isso garante que bibliotecas e suas versões não entrem em conflito com outros projetos que você tenha.<br>
Por exemplo, imagine que você possui um projeto que apenas roda com uma versão mais antiga de Python, mas o EchoCAD utiliza a última versão disponível atualmente (04-2026), sem o ambiente virtual você não conseguirá rodar este outro projeto ao atualizar globalmente a versão do seu Python.

Para criar o ambiente virtual utilize o seguinte comando:

```bash
python -m venv venv
```

Inicie seu ambiente virtual com:
```bash
venv\Scripts\activate
```

E para sair do ambiente virtual escreva:
```bash
deactivate
```
>Lembre-se sempre de iniciar o ambiente virtual antes de executar o projeto

Na pasta `app`, execute:<br>
> Obs: Você terá que instalar as dependências tanto do frontend quanto do backend, mas ambos partem dessa mesma pasta `app`.

### Frontend

Navegue até a pasta do frontend com o seguinte comando:

```bash
cd frontend
```

Para instalar as dependências utilize o comando:
```bash
npm install
```

> Não feche o terminal ainda, você terá que abrir dois deles para rodar completamente o projeto

### Backend

Abra outro terminal para executar as seguintes funções, caso esteja usando o CMD você terá que abrir outro, mas com o VS Code basta clicar no sinal de `+` na direita no botão `TERMINAL` e `PORTS`.

A partir da pasta `app` navegue até a pasta do backend

```bash
cd backend
```

Instale as dependências com o comando:
```bash
pip install -r requirements.txt
```

---

## pipx

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

# <span id="execucao-projeto">Execução do projeto</span>

Como dito anteriormente, utilize o mesmo método da instalação das dependências.

## venv

### Frontend

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

### Backend

```bash
uvicorn src.main:app --reload
```

---

### 3. Verifique os logs do servidor (frontend)

No terminal onde você executou `pnpm dev`, você deve ver:

```
✓ Ready in 2.5s
○ Compiling / ...
✓ Compiled / in 1.2s
```

---

## ▶️ Execução do Projeto com o pipx

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