from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.processamento import create_processamento, read_processamento, read_all_processamentos
from ...schemas.database import ProcessamentoCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['processamento'])


@router.post('/', summary='Criar processamento')
async def create_proc(proc: ProcessamentoCreate, db: Session = Depends(get_session)):
    return safe_create(create_processamento, db, proc, "Erro ao criar processamento")


@router.get('/', summary='Listar todos os processamentos')
async def list_processamentos(db: Session = Depends(get_session)):
    return safe_read(read_all_processamentos, db, "Erro ao buscar processamentos")


@router.get('/{processamento_id}', summary='Buscar processamento por ID')
async def get_processamento(processamento_id: int, db: Session = Depends(get_session)):
    return read_processamento(db, processamento_id)