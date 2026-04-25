from sqlalchemy.orm import Session
from src.models import DocumentoGerado
from ...schemas.database import DocumentoGeradoCreate


def create_documento_gerado(db: Session, documento: DocumentoGeradoCreate):
    new_documento = DocumentoGerado(**documento.model_dump())
    db.add(new_documento)
    db.commit()
    db.refresh(new_documento)
    return new_documento


def read_documento_gerado(db: Session, documento_id: int):
    return db.query(DocumentoGerado).filter(DocumentoGerado.id == documento_id).first()


def read_all_documentos_gerados(db: Session):
    return db.query(DocumentoGerado).all()
