from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.usuario import create_usuario, read_usuario, read_all_usuarios
from ...schemas.database import CreateUser
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['usuario'])


@router.post('/', summary='Criar usuário')
async def create_user(user: CreateUser, db: Session = Depends(get_session)):
    return safe_create(create_usuario, db, user, "Erro ao criar usuário")


@router.get('/', summary='Listar todos os usuários')
async def list_users(db: Session = Depends(get_session)):
    return safe_read(read_all_usuarios, db, "Erro ao buscar usuários")


@router.get('/{usuario_id}', summary='Buscar usuário por ID')
async def get_user(usuario_id: int, db: Session = Depends(get_session)):
    return read_usuario(db, usuario_id)