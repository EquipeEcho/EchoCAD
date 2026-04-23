from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_processamento
from ...schemas.database import ProcessamentoCreate
from ..helpers import safe_create

router = APIRouter(tags=['processamento'])


@router.post('/', summary='Criar processamento')
async def create_proc(proc: ProcessamentoCreate, db: Session = Depends(get_session)):
    return safe_create(create_processamento, db, proc, "Erro ao criar processamento")