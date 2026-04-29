from sqlalchemy.orm import Session

from src.models import Norma
from ...schemas.database.norma import NormaCreate


def create_norma(db: Session, norma: NormaCreate):
    new_norma = Norma(**norma.model_dump())
    db.add(new_norma)
    db.commit()
    db.refresh(new_norma)
    return new_norma


def read_norma(db: Session, norma_id: int):
    return db.query(Norma).filter(Norma.id == norma_id).first()


def read_all_normas(db: Session):
    return db.query(Norma).all()
