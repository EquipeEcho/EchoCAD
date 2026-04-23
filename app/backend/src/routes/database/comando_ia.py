from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_comando_ia
from ...schemas.database import ComandoIACreate
from ..helpers import safe_create

router = APIRouter(tags=['comando_ia'])


@router.post('/', summary='Criar comando IA')
async def create_comando(comando: ComandoIACreate, db: Session = Depends(get_session)):
    return safe_create(create_comando_ia, db, comando, "Erro ao criar comando IA")