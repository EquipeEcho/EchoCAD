from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.memorial_calculo import create_memorial_calculo, read_memorial_calculo, read_all_memoriais_calculo
from ...schemas.database import MemorialCalculoCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['memorial_calculo'])


@router.post('/', summary='Criar memorial de cálculo')
async def create_memorial(memorial: MemorialCalculoCreate, db: Session = Depends(get_session)):
    return safe_create(create_memorial_calculo, db, memorial, "Erro ao criar memorial de cálculo")


@router.get('/', summary='Listar todos os memoriais de cálculo')
async def list_memoriais(db: Session = Depends(get_session)):
    return safe_read(read_all_memoriais_calculo, db, "Erro ao buscar memoriais de cálculo")


@router.get('/{memorial_id}', summary='Buscar memorial de cálculo por ID')
async def get_memorial(memorial_id: int, db: Session = Depends(get_session)):
    return read_memorial_calculo(db, memorial_id)