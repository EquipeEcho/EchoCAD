from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_arquivo
from ...schemas.database import ArquivoCreate
from ..helpers import safe_create

router = APIRouter(tags=['arquivo'])


@router.post('/', summary='Criar arquivo')
async def create_arq(arquivo: ArquivoCreate, db: Session = Depends(get_session)):
    return safe_create(create_arquivo, db, arquivo, "Erro ao criar arquivo")