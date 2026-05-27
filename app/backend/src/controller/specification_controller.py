# src/controller/specification_controller.py

from sqlalchemy.orm import Session
from src.models.projeto_db import Specification


def criar_especificacao(db: Session, path: str, id_project: int) -> Specification:
    """
    Cria e salva uma nova instância da Especificação Técnica no banco de dados.
    """
    nova_spec = Specification(path=path, id_project=id_project)
    db.add(nova_spec)
    db.commit()
    db.refresh(nova_spec)

    return nova_spec
