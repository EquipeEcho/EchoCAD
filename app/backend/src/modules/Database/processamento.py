from sqlalchemy.orm import Session
from src.models import Processamento
from ...schemas.database.processamento import ProcessamentoCreate


def create_processamento(db: Session, proc: ProcessamentoCreate):
    new_proc = Processamento(**proc.model_dump())
    db.add(new_proc)
    db.commit()
    db.refresh(new_proc)
    return new_proc


def read_processamento(db: Session, processamento_id: int):
    return db.query(Processamento).filter(Processamento.id == processamento_id).first()


def read_all_processamentos(db: Session):
    return db.query(Processamento).all()
