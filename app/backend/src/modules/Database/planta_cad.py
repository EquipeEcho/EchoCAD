from sqlalchemy.orm import Session

from src.models import PlantaCad
from ...schemas.database.planta_cad import PlantaCadCreate


def create_planta_cad(db: Session, planta: PlantaCadCreate):
    new_planta = PlantaCad(**planta.model_dump())
    db.add(new_planta)
    db.commit()
    db.refresh(new_planta)
    return new_planta


def read_planta_cad(db: Session, planta_id: int):
    return db.query(PlantaCad).filter(PlantaCad.id == planta_id).first()


def read_all_plantas_cad(db: Session):
    return db.query(PlantaCad).all()
