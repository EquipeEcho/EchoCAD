# 📌 Guia de Comandos Essenciais do NPM

## 🛠️ Comandos do Dia a Dia (Fluxo de Trabalho)

*   **`npm init`**
    *   **O que faz:** Inicializa um novo projeto Node.js na pasta atual.
    *   **Para que serve:** Cria o arquivo `package.json` fazendo perguntas iniciais. Use `npm init -y` para pular as perguntas e aceitar o padrão.

*   **`npm install <nome-do-pacote>`** (Atalho: `npm i <nome-do-pacote>`)
    *   **O que faz:** Baixa e instala um pacote específico da internet.
    *   **Para que serve:** Adiciona uma nova biblioteca ao projeto. Salva os arquivos na pasta `node_modules`, registra a dependência no `package.json` e trava a versão no `package-lock.json`.

*   **`npm install`** (Sem especificar pacote)
    *   **O que faz:** Lê o seu `package.json` e instala todas as dependências listadas.
    *   **Para que serve:** Usado para recriar a pasta `node_modules` quando você clona um projeto do GitHub, por exemplo.

*   **`npm ci`** (Clean Install)
    *   **O que faz:** Deleta a pasta `node_modules` e instala tudo do zero baseando-se **estritamente** no `package-lock.json`.
    *   **Para que serve:** Garante uma instalação 100% idêntica à última vez que o projeto funcionou. Ideal para servidores, ambientes de produção ou ao retomar projetos antigos sem correr o risco de atualizações automáticas quebrarem o código.

---

## 🛡️ Comandos de Segurança e Auditoria

*   **`npm audit`**
    *   **O que faz:** Analisa o projeto e cruza os dados com o banco de vulnerabilidades do NPM.
    *   **Para que serve:** Exibe um relatório detalhado de falhas de segurança encontradas (Low, Moderate, High, Critical). **Não altera nenhum arquivo**, apenas reporta.

*   **`npm audit fix`**
    *   **O que faz:** Corrige automaticamente as vulnerabilidades que possuem atualizações seguras.
    *   **Para que serve:** Atualiza pacotes antigos para versões corrigidas, mas apenas se a atualização não contiver *Breaking Changes* (mudanças que quebram o código).

*   **`npm audit fix --force`**
    *   **O que faz:** Força a atualização de pacotes para remover vulnerabilidades, ignorando riscos de compatibilidade.
    *   **Para que serve:** Deve ser usado com cautela. Ele vai sumir com os avisos, mas pode atualizar pacotes para versões com grandes mudanças estruturais, correndo o risco de quebrar o funcionamento do seu projeto.

---

## 🧼 Comandos de Limpeza

*   **`npm cache clean --force`**
    *   **O que faz:** Limpa a pasta de cache local que o NPM mantém no seu computador.
    *   **Para que serve:** Serve para resolver bugs inexplicáveis ou arquivos corrompidos durante o download de pacotes, forçando o NPM a buscar tudo direto da internet novamente.