from sqlalchemy.ext.asyncio import AsyncSession
from src.models.projeto_db import Specification


async def criar_especificacao(db: AsyncSession, path: str, id_project: int) -> Specification:
    """
    Cria e salva uma nova instância da Especificação Técnica no banco de dados.
    """
    nova_spec = Specification(path=path, id_project=id_project)
    db.add(nova_spec)
    await db.commit()
    await db.refresh(nova_spec)

    return nova_spec
