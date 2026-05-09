from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.projeto_db import Blueprint
from src.schemas.user_schema import BlueprintSchema


def create_blueprint(db: Session, planta: BlueprintSchema) -> Blueprint:
    """
    Insere um novo registro de planta CAD no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.
        planta (BlueprintSchema): Objeto de esquema Pydantic contendo os dados da planta (tipo, arquivo, etc).

    Returns:
        Blueprint: A instância da planta persistida com os dados gerados pelo banco de dados.
    """
    new_planta = Blueprint(**planta.model_dump())
    db.add(new_planta)
    db.commit()
    db.refresh(new_planta)
    return new_planta


def read_planta_cad(db: Session, planta_id: int) -> Blueprint | None:
    """
    Busca uma planta CAD específica no banco de dados pelo seu ID.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.
        planta_id (int): Identificador único da planta.

    Returns:
        Blueprint | None: O objeto da planta se encontrado, ou None caso não exista no banco.
    """
    query = select(Blueprint).where(Blueprint.id == planta_id)
    return db.execute(query).scalar_one_or_none()


def read_all_blueprints(db: Session) -> list[Blueprint]:
    """
    Recupera todas as plantas CAD cadastradas no sistema.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.

    Returns:
        list[Blueprint]: Uma lista contendo todas as instâncias de plantas encontradas. 
                      Retorna uma lista vazia [] se não houver registros.
    """
    query = select(Blueprint)
    return list(db.execute(query).scalars().all())
