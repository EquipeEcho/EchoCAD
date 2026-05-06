from sqlalchemy import select
from sqlalchemy.orm import Session
from ..schemas.user_schema import StandardSchema
from ..models.projeto_db import Standard


def create_standard(db: Session, norma_schema: StandardSchema) -> Standard:
    """
    Instancia e persiste uma nova norma técnica no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy para operações de banco de dados.
        norma_schema (StandardSchema): Dados validados da norma provenientes do Pydantic.

    Returns:
        Standard: O objeto Standard recém-criado com os dados atualizados do banco (incluindo ID).
    """
    new_norma = Standard(**norma_schema.model_dump())
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
        Optional[Standard]: A instância da Standard se encontrada, ou None caso não exista.
    """
    query = select(Standard).where(Standard.id == norma_id)
    return db.execute(query).scalar_one_or_none()


def read_all_standards(db: Session):
    """
    Recupera todas as normas técnicas cadastradas no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.

    Returns:
        List[Standard]: Uma lista contendo todas as normas encontradas. 
                       Retorna uma lista vazia [] se não houver registros.
    """
    query = select(Standard)
    return list(db.execute(query).scalars().all())


def toggle_standard_status(db: Session, norma_id: int) -> Standard:
    """
    Alterna o status ativo/inativo de uma norma técnica.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.
        norma_id (int): O ID da norma a ser alterada.

    Returns:
        Standard: A norma atualizada.
        
    Raises:
        ValueError: Se a norma não for encontrada.
    """
    norma = read_norma(db, norma_id)
    if not norma:
        raise ValueError(f"Standard com ID {norma_id} não encontrada")
    
    norma.active = not norma.active
    db.commit()
    db.refresh(norma)
    return norma
