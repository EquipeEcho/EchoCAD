from sqlalchemy.orm import Session
from src.models import Calculo
from ...schemas.database.calculo import CalculoCreate


def create_calculo(db: Session, calc: CalculoCreate):
    new_calc = Calculo(**calc.model_dump())
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc


def read_calculo(db: Session, calculo_id: int):
    return db.query(Calculo).filter(Calculo.ID == calculo_id).first()


def read_all_calculos(db: Session):
    return db.query(Calculo).all()
