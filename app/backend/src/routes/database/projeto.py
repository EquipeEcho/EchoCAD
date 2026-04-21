from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_projeto
from ...schemas.database import ProjetoCreate
from ..helpers import safe_create

router = APIRouter(tags=['projeto'])


@router.post('/', summary='Criar projeto')
async def create_project(project: ProjetoCreate, db: Session = Depends(get_session)):
    return safe_create(create_projeto, db, project, "Erro ao criar projeto")