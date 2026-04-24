from sqlalchemy.orm import Session
from src.models import ComandoIA
from ...schemas.database.comando_ia import ComandoIACreate


def create_comando_ia(db: Session, comando: ComandoIACreate):
    new_comando = ComandoIA(**comando.model_dump())
    db.add(new_comando)
    db.commit()
    db.refresh(new_comando)
    return new_comando


def read_comando_ia(db: Session, comando_id: int):
    return db.query(ComandoIA).filter(ComandoIA.ID == comando_id).first()


def read_all_comandos_ia(db: Session):
    return db.query(ComandoIA).all()
