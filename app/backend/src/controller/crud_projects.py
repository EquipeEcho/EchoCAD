from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.projeto_db import Blueprint, Project, Report, Specification
from src.schemas.user_schema import CreateProjectSchema, UpdateProjectSchema


def create_projeto(db: Session, project_schema: CreateProjectSchema) -> Project:
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
    try:
        new_project = Project(**project_schema.model_dump())
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        logger.debug(f'Created new project {project_schema.model_dump()}')
        return new_project
    except IntegrityError as e:
        logger.error(e)
        raise ValueError('Algum campo informado possui valor incorreto, '
                         'para mais detalhes consulte o log.') from e


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


def update_project(db: Session, project_schema: UpdateProjectSchema) -> Project:
    """
    Atualiza os dados de um projeto existente no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.
        project_schema (UpdateProjectSchema): Dados validados para atualização.

    Returns:
        Projeto: O objeto do projeto atualizado.

    Raises:
        ValueError: Se o projeto com o ID fornecido não existir.
    """

    stmt = select(Project).where(Project.id == project_schema.id)
    existing_project = db.execute(stmt).scalar_one_or_none()

    if not existing_project:
        raise ValueError(f'Projeto com ID {project_schema.id} não encontrado.')

    for key, value in project_schema.model_dump(exclude_unset=True, exclude={'id'}).items():
        setattr(existing_project, key, value)

    db.commit()
    db.refresh(existing_project)
    return existing_project


def remove_project(db: Session, projeto_id: int) -> None:
    """
    Remove um projeto do banco de dados com base no seu ID.

    Args:
        db (Session): Sessão ativa do SQLAlchemy.
        projeto_id (int): O ID do projeto a ser deletado.

    Raises:
        ValueError: Se o projeto com o ID fornecido não existir.
    """
    stmt = select(Project).where(Project.id == projeto_id)
    existing_project = db.execute(stmt).scalar_one_or_none()

    if not existing_project:
        raise ValueError(f'Projeto com ID {projeto_id} não encontrado.')
    
    db.execute(delete(Report).where(Report.id_project == projeto_id))
    db.execute(delete(Blueprint).where(Blueprint.id_project == projeto_id))
    db.execute(delete(Specification).where(Specification.id_project == projeto_id))
    db.delete(existing_project)
    db.commit()
