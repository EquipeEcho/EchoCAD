from sqlalchemy.orm import Session

from src.models import ProjetoPlanta
from ...schemas.database.projeto_planta import ProjetoPlantaCreate


def create_projeto_planta(db: Session, projeto_planta: ProjetoPlantaCreate):
    new_projeto_planta = ProjetoPlanta(**projeto_planta.model_dump())
    db.add(new_projeto_planta)
    db.commit()
    db.refresh(new_projeto_planta)
    return new_projeto_planta


def read_projeto_planta(db: Session, id_projeto: int, id_planta: int):
    return (
        db.query(ProjetoPlanta)
        .filter(
            ProjetoPlanta.id_projeto == id_projeto,
            ProjetoPlanta.id_planta == id_planta,
        )
        .first()
    )


def read_all_projeto_planta(db: Session):
    return db.query(ProjetoPlanta).all()
