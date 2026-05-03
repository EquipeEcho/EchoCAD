from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..controller.projeto_crud import create_projeto, read_all_projetos, read_projeto
from ..database import get_session
from ..schemas.user_schema import ProjetoSchema, ProjectPublic
from ..schemas.system_schema import Success

router = APIRouter(prefix='/projeto', tags=['projeto'])


@router.post('/', summary='Criar projeto', status_code=status.HTTP_201_CREATED, response_model=ProjectPublic)
async def create_project(project_schema: ProjetoSchema, db: Session = Depends(get_session)):
    """
    Rota para criação de um novo projeto.
    """
    try:
        result = create_projeto(db, project_schema)
        return result

    except Exception as e:
        msg = 'Erro ao criar o projeto'
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")


@router.get('/', summary='Listar todos os projetos', status_code=status.HTTP_200_OK, response_model=List[ProjectPublic])
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
