from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...models.database.main import create_usuario
from ...schemas.database import UsuarioCreate
from ..helpers import safe_create

router = APIRouter(tags=['usuario'])


@router.post('/', summary='Criar usuário')
async def create_user(user: UsuarioCreate, db: Session = Depends(get_session)):
    return safe_create(create_usuario, db, user, "Erro ao criar usuário")