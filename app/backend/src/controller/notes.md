# CRUD

Aqui encontram-se os métodos de acesso direto ao banco de dados baseado
em modelos sqlalchemy. Para acessar o banco de dados primeiro ele deve
estar devidamente configurado:

- MySQL instalado na máquina ou em um container com a porta padrão exposta no localhost
- Usuário echocad_admin criado com a senha echocad_admin_password (senha padrão de teste)
- Banco de dados previamente criado 'echocad_db'
- Implementação da migration com o alembic para a criação automática das tabelas.