from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.comando_ia import create_comando_ia, read_comando_ia, read_all_comandos_ia
from ...schemas.database import ComandoIACreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['comando_ia'])


@router.post('/', summary='Criar comando IA')
async def create_comando(comando: ComandoIACreate, db: Session = Depends(get_session)):
    return safe_create(create_comando_ia, db, comando, "Erro ao criar comando IA")


@router.get('/', summary='Listar todos os comandos IA')
async def list_comandos(db: Session = Depends(get_session)):
    return safe_read(read_all_comandos_ia, db, "Erro ao buscar comandos IA")


@router.get('/{comando_id}', summary='Buscar comando IA por ID')
async def get_comando(comando_id: int, db: Session = Depends(get_session)):
    return read_comando_ia(db, comando_id)