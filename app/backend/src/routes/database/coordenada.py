from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.coordenada import create_coordenada, read_coordenada, read_all_coordenadas
from ...schemas.database import CoordenadaCreate
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['coordenada'])


@router.post('/', summary='Criar coordenada')
async def create_coord(coord: CoordenadaCreate, db: Session = Depends(get_session)):
    return safe_create(create_coordenada, db, coord, "Erro ao criar coordenada")


@router.get('/', summary='Listar todas as coordenadas')
async def list_coordenadas(db: Session = Depends(get_session)):
    return safe_read(read_all_coordenadas, db, "Erro ao buscar coordenadas")


@router.get('/{coordenada_id}', summary='Buscar coordenada por ID')
async def get_coordenada(coordenada_id: int, db: Session = Depends(get_session)):
    return read_coordenada(db, coordenada_id)