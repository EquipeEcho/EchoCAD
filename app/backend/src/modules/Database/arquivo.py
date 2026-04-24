from sqlalchemy.orm import Session
from src.models import Arquivo
from ...schemas.database.arquivo import ArquivoCreate


def create_arquivo(db: Session, arquivo: ArquivoCreate):
    new_arquivo = Arquivo(**arquivo.model_dump())
    db.add(new_arquivo)
    db.commit()
    db.refresh(new_arquivo)
    return new_arquivo


def read_arquivo(db: Session, arquivo_id: int):
    return db.query(Arquivo).filter(Arquivo.ID == arquivo_id).first()


def read_all_arquivos(db: Session):
    return db.query(Arquivo).all()
