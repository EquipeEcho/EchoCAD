from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_especificacao_tecnica
from ...schemas.database import EspecificacaoTecnicaCreate
from ..helpers import safe_create

router = APIRouter(tags=['especificacao_tecnica'])


@router.post('/', summary='Criar especificação técnica')
async def create_especificacao(espec: EspecificacaoTecnicaCreate, db: Session = Depends(get_session)):
    return safe_create(create_especificacao_tecnica, db, espec, "Erro ao criar especificação técnica")