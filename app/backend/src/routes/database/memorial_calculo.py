from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_memorial_calculo
from ...schemas.database import MemorialCalculoCreate
from ..helpers import safe_create

router = APIRouter(tags=['memorial_calculo'])


@router.post('/', summary='Criar memorial de cálculo')
async def create_memorial(memorial: MemorialCalculoCreate, db: Session = Depends(get_session)):
    return safe_create(create_memorial_calculo, db, memorial, "Erro ao criar memorial de cálculo")