from sqlalchemy.orm import Session
from src.models import EspecificacaoTecnica
from ...schemas.database.especificacao_tecnica import EspecificacaoTecnicaCreate


def create_especificacao_tecnica(db: Session, espec: EspecificacaoTecnicaCreate):
    new_espec = EspecificacaoTecnica(**espec.model_dump())
    db.add(new_espec)
    db.commit()
    db.refresh(new_espec)
    return new_espec


def read_especificacao_tecnica(db: Session, especificacao_id: int):
    return db.query(EspecificacaoTecnica).filter(EspecificacaoTecnica.id == especificacao_id).first()


def read_all_especificacoes_tecnicas(db: Session):
    return db.query(EspecificacaoTecnica).all()
