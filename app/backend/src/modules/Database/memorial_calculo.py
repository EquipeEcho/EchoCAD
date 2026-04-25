from sqlalchemy.orm import Session
from src.models import MemorialCalculo
from ...schemas.database.memorial_calculo import MemorialCalculoCreate


def create_memorial_calculo(db: Session, memorial: MemorialCalculoCreate):
    new_memorial = MemorialCalculo(**memorial.model_dump())
    db.add(new_memorial)
    db.commit()
    db.refresh(new_memorial)
    return new_memorial


def read_memorial_calculo(db: Session, memorial_id: int):
    return db.query(MemorialCalculo).filter(MemorialCalculo.id == memorial_id).first()


def read_all_memoriais_calculo(db: Session):
    return db.query(MemorialCalculo).all()
