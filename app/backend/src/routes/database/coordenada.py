from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_coordenada
from ...schemas.database import CoordenadaCreate
from ..helpers import safe_create

router = APIRouter(tags=['coordenada'])


@router.post('/', summary='Criar coordenada')
async def create_coord(coord: CoordenadaCreate, db: Session = Depends(get_session)):
    return safe_create(create_coordenada, db, coord, "Erro ao criar coordenada")