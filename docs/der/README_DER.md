# DIAGRAMA ENTIDADE RELACIONAMENTO
## Versão 2.0 - Modelo Simplificado que atende às necessidades do projeto

### 1. Entidade: Users
Responsável pelo acesso ao sistema e autoria dos projetos.

- id (PK): Identificador único.
- name: Nome completo do usuário.
- email: Endereço de e-mail (Login).
- password: Hash da senha para autenticação.
- created_at: Data de criação do usuário.

### 2. Entidade: Projects
O agrupador principal de todos os arquivos e memoriais.

- id (PK): Identificador único.
- name: Nome da obra ou serviço.
- description: Detalhamento do escopo do projeto.
- client: Nome do cliente que requisitou o projeto.
- created_at: Timestamp de quando o projeto foi aberto.

### 3. Entidade: Blueprint
Metadados do arquivo técnico processado pelo Python.

- id (PK): Identificador único.
- discipline: Nome do tipo de arquivo da planta CAD
- path: Path ou URL onde o arquivo está armazenado no servidor.

### 4. Entidade: Reports
Memorial de cálculo gerado pelo software.

- id (PK): Identificador único.
- path: Path ou URL onde o arquivo está armazenado no servidor.

### 5. Entidade: Specifications
O documento da especificação técnica final gerado pelo software.

- id (PK): Identificador único.
- path: Path ou URL onde o arquivo está armazenado no servidor.