from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.elemento import create_elemento, read_elemento, read_all_elementos
from ...schemas.database import ElementoCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['elemento'])


@router.post('/', summary='Criar elemento')
async def create_elem(elem: ElementoCreate, db: Session = Depends(get_session)):
    return safe_create(create_elemento, db, elem, "Erro ao criar elemento")


@router.get('/', summary='Listar todos os elementos')
async def list_elementos(db: Session = Depends(get_session)):
    return safe_read(read_all_elementos, db, "Erro ao buscar elementos")


@router.get('/{elemento_id}', summary='Buscar elemento por ID')
async def get_elemento(elemento_id: int, db: Session = Depends(get_session)):
    return read_elemento(db, elemento_id)