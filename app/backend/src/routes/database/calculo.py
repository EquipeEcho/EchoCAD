from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_calculo
from ...schemas.database import CalculoCreate
from ..helpers import safe_create

router = APIRouter(tags=['calculo'])


@router.post('/', summary='Criar cálculo')
async def create_calc(calc: CalculoCreate, db: Session = Depends(get_session)):
    return safe_create(create_calculo, db, calc, "Erro ao criar cálculo")