# Scripts de Desenvolvimento - EchoCAD Backend

Este diretório contém scripts auxiliares para configurar e manter o ambiente de desenvolvimento do backend EchoCAD.

---

## 📋 Índice

1. [configurar_ambiente.py](#configurar_ambientepy)
2. [reset_database.py](#reset_databasepy)

---

## configurar_ambiente.py

### O que faz?

Script interativo para configurar o ambiente de desenvolvimento completo do EchoCAD. Automatiza a instalação e atualização de ferramentas essenciais necessárias para rodar o projeto.

### Principais funções:

1. **Instala/atualiza pipx** - Gerenciador de pacotes Python isolado
2. **Instala/atualiza uv** - Gerenciador de pacotes ultra-rápido (substitui pip)
3. **Executa `uv sync`** - Sincroniza e instala todas as dependências do projeto
4. **Fornece instruções** - Guia para configurar o interpretador Python no VS Code

### Como usar?

#### Opção 1: Executar com Python diretamente
```bash
python dev/configurar_ambiente.py
```

#### Opção 2: Executar com permissão de execução (Linux/Mac)
```bash
chmod +x dev/configurar_ambiente.py
./dev/configurar_ambiente.py
```

#### Opção 3: Executar pelo uv (após configuração inicial)
```bash
uv run dev/configurar_ambiente.py
```

### Fluxo de execução:

1. **Verifica pipx**
   - Se não estiver instalado, pergunta se deseja instalar
   - Se estiver desatualizado, pergunta se deseja atualizar

2. **Verifica uv**
   - Se não estiver instalado, pergunta se deseja instalar via pipx
   - Se estiver desatualizado, tenta atualizar via pipx

3. **Executa `uv sync`**
   - Navega para o diretório `src`
   - Instala todas as dependências do `pyproject.toml`

4. **Mostra instruções finais**
   - Caminho do virtual environment (.venv)
   - Como configurar o interpretador no VS Code
   - Comandos úteis para desenvolvimento

### Requisitos:

- Python 3.8+ instalado
- Acesso à internet (para verificar versões mais recentes)

### Plataformas suportadas:

- ✅ Windows (otimizado)
- ✅ Linux/Mac (com avisos)

---

## reset_database.py

### O que faz?

Script para resetar completamente o banco de dados MySQL do EchoCAD. Remove todas as tabelas existentes e recria o banco de dados e usuário do zero, preparando-o para novas migrações via Alembic.

### Principais funções:

1. **Cria banco de dados** - Se não existir
2. **Cria usuário do banco** - `echocad_admin` com permissões apropriadas
3. **Remove todas as tabelas** - Limpa o banco completamente
4. **Configura permissões** - Garante que o usuário tem acesso correto

### Como usar?

#### Executar o script:
```bash
python dev/reset_database.py
```

#### Ou com uv (após ambiente configurado):
```bash
uv run dev/reset_database.py
```

### Fluxo de execução:

1. **Lê configuração do banco**
   - Obtém dados de conexão do arquivo `src/config.py`
   - Exibe host, porta e nome do banco

2. **Solicita credenciais admin**
   - Pede usuário admin do MySQL (padrão: `root`)
   - Pede senha do admin (entrada oculta por segurança)

3. **Cria banco e usuário**
   - Cria banco se não existir: `echocad`
   - Cria usuário: `echocad_admin`
   - Concede permissões adequadas (sem permissão de DROP DATABASE)

4. **Remove todas as tabelas**
   - Lista todas as tabelas existentes
   - Desabilita verificação de chaves estrangeiras
   - Remove cada tabela
   - Reabilita verificação de chaves estrangeiras

5. **Mensagem de sucesso**
   - Confirma que o banco está pronto para novas migrações

### Requisitos:

- MySQL/MariaDB rodando localmente ou acessível
- Credenciais de admin do MySQL disponíveis
- Pacote Python `pymysql` instalado

### Configuração esperada:

O script lê as configurações de:
```
app/backend/src/config.py
```

A URL do banco deve estar configurada em `settings.database_url`

### Segurança:

- ⚠️ **Aviso**: Este script REMOVE TODOS OS DADOS do banco
- A senha de admin é solicitada sem echo na tela
- As credenciais do banco são criadas automaticamente

---

## 🔄 Fluxo completo de configuração

### Primeira vez configurando o projeto:

```bash
# 1. Navegar para o diretório backend
cd app/backend

# 2. Configurar o ambiente
python dev/configurar_ambiente.py

# 3. Seguir as instruções para configurar VS Code

# 4. (Opcional) Resetar o banco de dados se precisar
python dev/reset_database.py
```

### Após mudanças no banco (migrações):

```bash
# 1. Resetar o banco de dados
python dev/reset_database.py

# 2. Executar as migrações do Alembic
uv run alembic upgrade head

# 3. Iniciar o servidor
uv run fastapi dev src/main.py
```

---

## 🆘 Solução de problemas

### "pipx: comando não encontrado"
- Instale Python: https://www.python.org/downloads/
- Ou execute: `python -m pip install pipx`

### "uv: comando não encontrado"
- Execute o script de configuração: `python dev/configurar_ambiente.py`
- Ou instale manualmente: `pipx install uv`

### Erro ao conectar ao MySQL
- Verifique se MySQL está rodando
- Confirme as credenciais de admin
- Confira a URL do banco em `src/config.py`

### "pymysql.Error: (1045, "Access denied...)"
- Verifique a senha de admin do MySQL
- Certifique-se de ter acesso ao host configurado

### Dependências não instaladas
- Execute novamente: `python dev/configurar_ambiente.py`
- Ou manualmente: `uv sync` (dentro do diretório `src`)
