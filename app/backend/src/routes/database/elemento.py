from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_elemento
from ...schemas.database import ElementoCreate
from ..helpers import safe_create

router = APIRouter(tags=['elemento'])


@router.post('/', summary='Criar elemento')
async def create_elem(elem: ElementoCreate, db: Session = Depends(get_session)):
    return safe_create(create_elemento, db, elem, "Erro ao criar elemento")