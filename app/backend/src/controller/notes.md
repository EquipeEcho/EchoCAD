# CRUD

Aqui encontram-se os métodos de acesso direto ao banco de dados baseado
em modelos sqlalchemy. Para acessar o banco de dados ele deve estar devidamente configurado:

- MySQL instalado na máquina ou em um container com a porta padrão exposta no localhost
- Usuário echocad_admin criado com a senha echocad_admin_password (senha padrão de teste)
- Banco de dados previamente criado 'echocad_db'
- Implementação da migration com o alembic para a criação automática das tabelas.

### Modulos

- crud_projects: para manipulação dos registros de projetos.
- crud_blueprints: crud para manipulação dos registros de plantas de cad.
- crud_standards: manipulação de normas técnicas do sistema.
- crud_users: manipulação do registro de usuários.