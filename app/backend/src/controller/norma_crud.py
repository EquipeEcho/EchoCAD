from sqlalchemy import select
from sqlalchemy.orm import Session
from ..schemas.user_schema import NormaSchema
from ..models.projeto_db import Norma


def create_norma(db: Session, norma_schema: NormaSchema) -> Norma:
    """
    Instancia e persiste uma nova norma técnica no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy para operações de banco de dados.
        norma_schema (NormaSchema): Dados validados da norma provenientes do Pydantic.

    Returns:
        Norma: O objeto Norma recém-criado com os dados atualizados do banco (incluindo ID).
    """
    new_norma = Norma(**norma_schema.model_dump())
    db.add(new_norma)
    db.commit()
    db.refresh(new_norma)
    return new_norma


def read_norma(db: Session, norma_id: int):
    """
    Busca uma norma técnica específica através de seu identificador único (ID).

    Args:
        db (Session): Sessão ativa do SQLAlchemy.
        norma_id (int): O ID primário da norma a ser recuperada.

    Returns:
        Optional[Norma]: A instância da Norma se encontrada, ou None caso não exista.
    """
    query = select(Norma).where(Norma.id == norma_id)
    return db.execute(query).scalar_one_or_none()


def read_all_normas(db: Session):
    """
    Recupera todas as normas técnicas cadastradas no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.

    Returns:
        List[Norma]: Uma lista contendo todas as normas encontradas. 
                       Retorna uma lista vazia [] se não houver registros.
    """
    query = select(Norma)
    return list(db.execute(query).scalars().all())
