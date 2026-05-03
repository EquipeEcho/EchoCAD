from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_session
from ...modules.Database.usuario import create_usuario, read_usuario, read_all_usuarios, authenticate_usuario
from ...schemas.database import CreateUser, LoginUser
from ..helpers import safe_create, safe_read

router = APIRouter(tags=['usuario'])


@router.post('/', summary='Criar usuário')
async def create_user(user: CreateUser, db: Session = Depends(get_session)):
    return safe_create(create_usuario, db, user, "Erro ao criar usuário")


# implementação futura
# @router.get('/', summary='Listar todos os usuários')
# async def list_users(db: Session = Depends(get_session)):
#     return safe_read(read_all_usuarios, db, "Erro ao buscar usuários")


# verificar depois
# @router.get('/{usuario_id}', summary='Buscar usuário por ID')
# async def get_user(usuario_id: int, db: Session = Depends(get_session)):
#     return read_usuario(db, usuario_id)


@router.post('/login', summary='Login de usuário')
async def login_user(credentials: LoginUser, db: Session = Depends(get_session)):
    user = authenticate_usuario(db, credentials.email, credentials.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )

    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "message": "Login realizado com sucesso",
    }