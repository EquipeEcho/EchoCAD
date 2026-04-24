from sqlalchemy.orm import Session
from src.models import Project
from ...schemas.database.projeto import ProjetoCreate


def create_projeto(db: Session, project: ProjetoCreate):
    new_project = Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def read_projeto(db: Session, projeto_id: int):
    return db.query(Project).filter(Project.ID == projeto_id).first()


def read_all_projetos(db: Session):
    return db.query(Project).all()
