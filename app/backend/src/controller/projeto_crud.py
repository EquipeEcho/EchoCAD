from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_session
from ..models.projeto_db import Project
from ..schemas.user_schema import ProjetcSchema


def create_projeto(db: Session, project_schema: ProjetcSchema) -> Project:
    """
    Instancia e persiste um novo projeto no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.
        project_schema (ProjetoCreate): Dados validados do projeto via Pydantic.

    Returns:
        Projeto: O objeto do projeto persistido, incluindo IDs e timestamps gerados.

    Raises:
        SQLAlchemyError: Caso ocorra uma falha na persistência dos dados.
    """
    new_project = Project(**project_schema.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def read_projeto(db: Session, projeto_id: int) -> Project | None:
    """
    Busca um projeto no banco de dados através do seu identificador único.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.
        projeto_id (int): O ID primário do projeto a ser recuperado.

    Returns:
        Optional[Projeto]: A instância do Projeto se encontrada, 
                           ou None caso o ID não exista.
    """
    query = select(Project).where(Project.id == projeto_id)
    return db.execute(query).scalar_one_or_none()


def read_all_projetos(db: Session) -> list[Project]:
    """
    Recupera todos os registros de projetos armazenados no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.

    Returns:
        List[Projeto]: Uma lista contendo todos os projetos encontrados. 
                       Retorna uma lista vazia [] se não houver registros.
    """
    query = select(Project)
    return list(db.execute(query).scalars().all())
