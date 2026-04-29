from sqlalchemy.orm import Session
from src.models import Projeto
from ...schemas.database.projeto import ProjetoCreate


def create_projeto(db: Session, project: ProjetoCreate):
    new_project = Projeto(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def read_projeto(db: Session, projeto_id: int):
    return db.query(Projeto).filter(Projeto.id == projeto_id).first()


def read_all_projetos(db: Session):
    return db.query(Projeto).all()
