from sqlalchemy.orm import Session

from src.models import ProjetoNorma
from ...schemas.database.projeto_norma import ProjetoNormaCreate


def create_projeto_norma(db: Session, projeto_norma: ProjetoNormaCreate):
    new_projeto_norma = ProjetoNorma(**projeto_norma.model_dump())
    db.add(new_projeto_norma)
    db.commit()
    db.refresh(new_projeto_norma)
    return new_projeto_norma


def read_projeto_norma(db: Session, id_projeto: int, id_norma: int):
    return (
        db.query(ProjetoNorma)
        .filter(
            ProjetoNorma.id_projeto == id_projeto,
            ProjetoNorma.id_norma == id_norma,
        )
        .first()
    )


def read_all_projeto_norma(db: Session):
    return db.query(ProjetoNorma).all()
