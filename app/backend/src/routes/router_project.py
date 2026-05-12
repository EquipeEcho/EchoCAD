from loguru import logger
from pathlib import Path
import shutil

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.controller.crud_projects import create_projeto, read_all_projetos, read_projeto, update_project
from src.database import get_session
from src.schemas.user_schema import CreateProjectSchema, ProjectPublicSchema, UpdateProjectSchema
from src.models.projeto_db import Project, Blueprint, Report, Specification
from deprecated import deprecated

router = APIRouter(prefix='/project', tags=['projeto'])


@router.post('/', summary='Criar projeto', status_code=status.HTTP_201_CREATED, response_model=ProjectPublicSchema)
async def post_create_project(project_schema: CreateProjectSchema, db: Session = Depends(get_session)):
    """
    Rota para criação de um novo projeto.
    """

    try:
        result = create_projeto(db, project_schema)
        logger.info(result)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Incorrect value error: {e}'
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {e}'
        ) from e


@router.get('/', summary='Listar todos os projetos', status_code=status.HTTP_200_OK, response_model=list[ProjectPublicSchema])
async def get_list_projects(db: Session = Depends(get_session)):
    """
    Rota para listar todos os projetos existentes.
    """
    try:
        result = read_all_projetos(db)
        return result

    except Exception as e:
        msg = 'Erro ao buscar os projetos existentes'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get('/', summary='Buscar projeto por ID', status_code=status.HTTP_200_OK, response_model=ProjectPublicSchema)
async def get_project(projeto_id: int, db: Session = Depends(get_session)):
    """
    Rota para buscar um projeto específico pelo seu ID.
    """
    try:
        result = read_projeto(db, projeto_id)
        if not result:
            raise HTTPException(
                status_code=404, detail="Projeto não encontrado")
        return result

    except HTTPException:
        raise
    except Exception as e:
        msg = 'Erro ao buscar o projeto'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.patch('/', summary='Atualizar projeto', status_code=status.HTTP_200_OK, response_model=ProjectPublicSchema)
async def patch_update_project(projeto_id: int, project_schema: UpdateProjectSchema, db: Session = Depends(get_session)):
    """
    Rota para atualizar um projeto existente.
    """

    try:
        return update_project(db, projeto_id, project_schema)

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        msg = 'Erro ao atualizar o projeto'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


# TODO: implementar validação.
@deprecated(reason='Essa rota não tem segurança e será substituída por uma com validação')
@router.delete('/', summary='Deletar projeto', status_code=status.HTTP_200_OK)
async def delete_project(projeto_id: int, db: Session = Depends(get_session)):
    """
    Rota para deletar um projeto e seus arquivos associados.
    - Remove referências de normas (tabela projeto_norma)
    - Remove memoriais de cálculo
    - Remove plantas CAD
    - Remove especificações técnicas
    - Remove o projeto do banco de dados
    - Renomeia a pasta de uploads para {project_id}.deleted
    """
    try:
        # Verifica se projeto existe
        projeto = db.query(Project).filter(Project.id == projeto_id).first()
        if not projeto:
            raise HTTPException(
                status_code=404, detail="Projeto não encontrado")

        # Remove todos os memoriais de cálculo
        db.query(Report).filter(Report.id_project == projeto_id).delete()

        # Remove todas as plantas CAD
        db.query(Blueprint).filter(Blueprint.id_project == projeto_id).delete()

        # Remove todas as especificações técnicas
        db.query(Specification).filter(
            Specification.id_project == projeto_id).delete()

        # Remove o projeto
        db.delete(projeto)
        db.commit()

        # Renomeia a pasta de uploads de {project_id} para {project_id}.deleted
        backend_root = Path(__file__).parent.parent.parent
        uploads_dir = backend_root / "uploads"
        project_folder = uploads_dir / str(projeto_id)
        deleted_folder = uploads_dir / f"{projeto_id}.deleted"

        if project_folder.exists():
            # Se a pasta .deleted já existe, remove antes
            if deleted_folder.exists():
                shutil.rmtree(deleted_folder)
            # Renomeia a pasta
            project_folder.rename(deleted_folder)

        return {
            "message": "Projeto deletado com sucesso",
            "projeto_id": projeto_id,
            "folder_status": "renomeada para .deleted" if project_folder.exists() or deleted_folder.exists() else "não encontrada"
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        msg = 'Erro ao deletar o projeto'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")
