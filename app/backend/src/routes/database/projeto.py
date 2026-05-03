from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.projeto import create_projeto, read_projeto, read_all_projetos
from ...schemas.database import ProjetoCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['projeto'])


@router.post('/', summary='Criar projeto')
async def create_project(project: ProjetoCreate, db: Session = Depends(get_session)):
    return safe_create(create_projeto, db, project, "Erro ao criar projeto")


@router.get('/', summary='Listar todos os projetos')
async def list_projects(db: Session = Depends(get_session)):
    return safe_read(read_all_projetos, db, "Erro ao buscar projetos")

# desabilitado por enquanto
# @router.get('/{projeto_id}', summary='Buscar projeto por ID')
# async def get_project(projeto_id: int, db: Session = Depends(get_session)):
#     return read_projeto(db, projeto_id)