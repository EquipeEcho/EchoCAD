# Alembic Migrations para EchoCAD

Este diretório contém todas as migrações de banco de dados do EchoCAD, gerenciadas pelo Alembic.

## Migrações Existentes

### 1. `bff4dbc79b56_inicializaçao_do_banco_de_dados.py`
**Descrição**: Cria o schema inicial com todas as tabelas principais

**Tabelas criadas:**
- `usuario` - Usuários do sistema
- `projeto` - Projetos CAD
- `normas` - Normas técnicas
- `projeto_norma` - Associação projeto ↔ normas
- `planta_cad` - Plantas CAD por projeto
- `especificacao_tecnica` - Especificações técnicas
- `memorial_calculo` - Memórias de cálculo (arquivos Excel)

**Relacionamentos:**
- Projeto → Usuario (1:N)
- Projeto → Planta_CAD (1:N)
- Projeto → Especificacao_Tecnica (1:N)
- Projeto → Memorial_Calculo (1:N)
- Projeto ↔ Normas (N:M via projeto_norma)

---

### 2. `10e6345c7312_ajusta_relacionamentos_e_adiciona_id_.py`
**Descrição**: Ajusta relacionamentos e adiciona campo `id_user` à tabela `projeto`

**Mudanças:**
- Adiciona coluna `id_user` em `projeto`
- Cria foreign key para `usuario.id`
- Melhor rastreabilidade de projetos por usuário

---

## Como Usar

### Ver Migrações
```bash
# Liste todas as migrações
alembic history

# Veja a versão atual
alembic current
```

### Executar Migrações (Automático no Docker)
```bash
# No container
docker-compose exec echocad_alembic alembic upgrade head

# Localmente
alembic upgrade head
```

### Criar Nova Migração
```bash
# Autogenerate (detecta mudanças em modelos)
alembic revision --autogenerate -m "Descrição da mudança"

# Manual (para customizações)
alembic revision -m "Descrição da mudança"
```

### Reverter Migrações
```bash
# Voltar uma versão
alembic downgrade -1

# Voltar para versão específica
alembic downgrade <revision_id>
```

---

## Estrutura de Migração

Cada arquivo de migração contém:

```python
# revision IDs
revision: str = '10e6345c7312'
down_revision: str = 'bff4dbc79b56'

# Função para aplicar migração (upgrade)
def upgrade() -> None:
    # Comandos SQL/DDL

# Função para desfazer migração (downgrade)
def downgrade() -> None:
    # Desfazer os comandos
```

---

## Fonte de Verdade

As migrações são geradas a partir de `src/models/projeto_db.py`:

```python
# Em src/models/projeto_db.py
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"
    # ... colunas

class Projeto(Base):
    __tablename__ = "projeto"
    # ... colunas
```

Quando modelos mudam, execute:
```bash
alembic revision --autogenerate -m "Descrição"
```

---

## Docker Compose

No docker-compose.yaml, o serviço `alembic-migrate`:
- ✅ Aguarda MySQL estar saudável
- ✅ Roda `alembic upgrade head` automaticamente
- ✅ Cria todas as tabelas antes da API iniciar

---

## Troubleshooting

### Migração falhou?
```bash
# Ver logs
docker-compose logs echocad_alembic

# Reiniciar
docker-compose restart echocad_alembic
```

### Conflito de migrações?
```bash
# Ver histórico
alembic history -v

# Se houver branches, mescle manualmente
```

### Schema desincronizado?
```bash
# Remova tudo e recomece
docker-compose down -v
docker-compose up -d
```

---

## Referências

- [Documentação Alembic](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- Modelos: `app/backend/src/models/projeto_db.py`
