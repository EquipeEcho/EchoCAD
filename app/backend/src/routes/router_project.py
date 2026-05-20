from loguru import logger
from pathlib import Path
import shutil

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.controller.crud_projects import (
    create_projeto,
    read_all_projetos,
    read_projeto,
    remove_project,
    update_project,
)
from src.database import get_session
from src.schemas.user_schema import (
    CreateProjectSchema,
    ProjectPublicSchema,
    UpdateProjectSchema,
)

router = APIRouter(prefix="/project", tags=["projeto"])


@router.post(
    "/",
    summary="Criar projeto",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectPublicSchema,
)
async def post_create_project(
    project_schema: CreateProjectSchema, db: Session = Depends(get_session)
):
    """
    Rota para criação de um novo projeto.
    """

    try:
        result = create_projeto(db, project_schema)
        logger.info(f"Projeto criado: {result}")
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incorrect value error: {e}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {e}",
        ) from e


@router.get(
    "/all",
    summary="Listar todos os projetos",
    status_code=status.HTTP_200_OK,
    response_model=list[ProjectPublicSchema],
)
async def get_list_projects(db: Session = Depends(get_session)):
    """
    Rota para listar todos os projetos existentes.
    """
    try:
        result = read_all_projetos(db)
        logger.info(f"Projetos encontrados: {len(result)}")
        return result

    except Exception as e:
        logger.error(f"Erro ao buscar os projetos existentes: {e}")
        raise HTTPException(
            status_code=500, detail="Erro ao buscar os projetos existentes"
        )


@router.get(
    "/",
    summary="Buscar projeto por ID",
    status_code=status.HTTP_200_OK,
    response_model=ProjectPublicSchema,
)
async def get_project(projeto_id: int, db: Session = Depends(get_session)):
    """
    Rota para buscar um projeto específico pelo seu ID.
    """
    try:
        result = read_projeto(db, projeto_id)
        if not result:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        logger.info(f"Projeto encontrado: {result}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar o projeto: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar o projeto")


@router.patch(
    "/",
    summary="Atualizar projeto",
    status_code=status.HTTP_200_OK,
    response_model=ProjectPublicSchema,
)
async def patch_update_project(
    project_schema: UpdateProjectSchema, db: Session = Depends(get_session)
):
    """
    Rota para atualizar um projeto existente.
    """

    try:
        logger.info(
            f"Atualizando projeto ID {project_schema.id} com dados: {project_schema}"
        )
        return update_project(db, project_schema)

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar o projeto: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar o projeto")


# TODO: implementar validação.
@router.delete("/", summary="Deletar projeto", status_code=status.HTTP_204_NO_CONTENT)
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
        remove_project(db, projeto_id)
        logger.info(f"Projeto ID {projeto_id} deletado com sucesso.")
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

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar o projeto: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar o projeto")
