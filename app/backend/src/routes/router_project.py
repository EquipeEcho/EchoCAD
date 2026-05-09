from pathlib import Path
import shutil

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.controller.crud_projects import create_projeto, read_all_projetos, read_projeto
from src.database import get_session
from src.schemas.user_schema import ProjetcSchema, ProjectPublic
from src.models.projeto_db import Project, Blueprint, Report, Specification
from deprecated import deprecated

router = APIRouter(prefix='/projeto', tags=['projeto'])


@router.post('/', summary='Criar projeto', status_code=status.HTTP_201_CREATED, response_model=ProjectPublic)
async def create_project(project_schema: ProjetcSchema, db: Session = Depends(get_session)):
    """
    Rota para criação de um novo projeto.
    """
    try:
        result = create_projeto(db, project_schema)
        return result

    except Exception as e:
        msg = 'Erro ao criar o projeto'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get('/', summary='Listar todos os projetos', status_code=status.HTTP_200_OK, response_model=list[ProjectPublic])
async def list_projects(db: Session = Depends(get_session)):
    """
    Rota para listar todos os projetos existentes.
    """
    try:
        result = read_all_projetos(db)
        return result

    except Exception as e:
        msg = 'Erro ao buscar os projetos existentes'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get('/{projeto_id}', summary='Buscar projeto por ID', status_code=status.HTTP_200_OK, response_model=ProjectPublic)
async def get_project(projeto_id: int, db: Session = Depends(get_session)):
    """
    Rota para buscar um projeto específico pelo seu ID.
    """
    try:
        result = read_projeto(db, projeto_id)
        if not result:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        return result

    except HTTPException:
        raise
    except Exception as e:
        msg = 'Erro ao buscar o projeto'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


# TODO: implementar validação.
@deprecated(reason='Essa rota não tem segurança e será substituída por uma com validação')
@router.delete('/{projeto_id}', summary='Deletar projeto', status_code=status.HTTP_200_OK)
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
            raise HTTPException(status_code=404, detail="Projeto não encontrado")

        # Remove todos os memoriais de cálculo
        db.query(Report).filter(Report.id_project == projeto_id).delete()

        # Remove todas as plantas CAD
        db.query(Blueprint).filter(Blueprint.id_project == projeto_id).delete()

        # Remove todas as especificações técnicas
        db.query(Specification).filter(Specification.id_project == projeto_id).delete()

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
