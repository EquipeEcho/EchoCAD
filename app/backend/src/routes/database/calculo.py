from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.calculo import create_calculo, read_calculo, read_all_calculos
from ...schemas.database import CalculoCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['calculo'])


@router.post('/', summary='Criar cálculo')
async def create_calc(calc: CalculoCreate, db: Session = Depends(get_session)):
    return safe_create(create_calculo, db, calc, "Erro ao criar cálculo")


@router.get('/', summary='Listar todos os cálculos')
async def list_calculos(db: Session = Depends(get_session)):
    return safe_read(read_all_calculos, db, "Erro ao buscar cálculos")


@router.get('/{calculo_id}', summary='Buscar cálculo por ID')
async def get_calculo(calculo_id: int, db: Session = Depends(get_session)):
    return read_calculo(db, calculo_id)