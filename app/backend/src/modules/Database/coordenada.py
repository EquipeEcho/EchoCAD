from sqlalchemy.orm import Session
from src.models import Coordenada
from ...schemas.database.coordenada import CoordenadaCreate


def create_coordenada(db: Session, coord: CoordenadaCreate):
    new_coord = Coordenada(**coord.model_dump())
    db.add(new_coord)
    db.commit()
    db.refresh(new_coord)
    return new_coord


def read_coordenada(db: Session, coordenada_id: int):
    return db.query(Coordenada).filter(Coordenada.id == coordenada_id).first()


def read_all_coordenadas(db: Session):
    return db.query(Coordenada).all()
