from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.projeto_db import Blueprint
from src.schemas.user_schema import BlueprintSchema


async def create_blueprint(db: AsyncSession, planta: BlueprintSchema) -> Blueprint:
    """
    Insere um novo registro de planta CAD no banco de dados.

    Args:
        db (AsyncSession): Sessão ativa do SQLAlchemy.
        planta (BlueprintSchema): Objeto de esquema Pydantic contendo os dados da planta (tipo, arquivo, etc).

    Returns:
        Blueprint: A instância da planta persistida com os dados gerados pelo banco de dados.
    """
    new_planta = Blueprint(**planta.model_dump())
    db.add(new_planta)
    await db.commit()
    await db.refresh(new_planta)
    return new_planta


async def read_planta_cad(db: AsyncSession, planta_id: int) -> Blueprint | None:
    """
    Busca uma planta CAD específica no banco de dados pelo seu ID.

    Args:
        db (AsyncSession): Sessão ativa do SQLAlchemy.
        planta_id (int): Identificador único da planta.

    Returns:
        Blueprint | None: O objeto da planta se encontrado, ou None caso não exista no banco.
    """
    query = select(Blueprint).where(Blueprint.id == planta_id)
    return (await db.execute(query)).scalar_one_or_none()


async def read_all_blueprints(db: AsyncSession) -> list[Blueprint]:
    """
    Recupera todas as plantas CAD cadastradas no sistema.

    Args:
        db (AsyncSession): Sessão ativa do SQLAlchemy.

    Returns:
        list[Blueprint]: Uma lista contendo todas as instâncias de plantas encontradas.
                      Retorna uma lista vazia [] se não houver registros.
    """
    query = select(Blueprint)
    return list((await db.execute(query)).scalars().all())
