from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_session
from src.schemas.user_schema import CreateUser, LoginUser, UserPublic
from src.controller.crud_users import get_user_by_email, create_user

router = APIRouter(prefix='/users', tags=["Users"])


@router.post('login', status_code=status.HTTP_200_OK)
async def route_login(data: LoginUser, session: Session = Depends(get_session)):
    '''
    Endpoint para autenticação de usuários.
    Args:
        data (LoginUser): Esquema de login contendo email e senha do usuário.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.
    '''
    user = get_user_by_email(session, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            # headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Login successful"} # TODO: implementar token JWT para autenticação


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def route_create_user(user: CreateUser, session: Session = Depends(get_session)):
    try:
        new_user = create_user(session, user)
        return UserPublic(
            name=new_user.name,
            email=new_user.email,
            created_at=new_user.created_at,
            message="User created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )
