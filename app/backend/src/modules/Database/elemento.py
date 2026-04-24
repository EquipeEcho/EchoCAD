from sqlalchemy.orm import Session
from src.models import Elemento
from ...schemas.database.elemento import ElementoCreate


def create_elemento(db: Session, elem: ElementoCreate):
    new_elem = Elemento(**elem.model_dump())
    db.add(new_elem)
    db.commit()
    db.refresh(new_elem)
    return new_elem


def read_elemento(db: Session, elemento_id: int):
    return db.query(Elemento).filter(Elemento.ID == elemento_id).first()


def read_all_elementos(db: Session):
    return db.query(Elemento).all()
