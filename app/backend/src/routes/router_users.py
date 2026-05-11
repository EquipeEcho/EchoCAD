from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_session
from src.schemas.user_schema import (
    CreateUserSchema,
    LoginUserSchema,
    UpdateUserSchema,
    UserPublicSchema,
)
from src.controller.crud_users import get_user_by_email, create_user, update_user

router = APIRouter(prefix='/users', tags=["Users"])


@router.post('/login', status_code=status.HTTP_200_OK, response_model=UserPublicSchema)
async def route_login(data: LoginUserSchema, session: Session = Depends(get_session)):
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
    # TODO: implementar token JWT para autenticação
    return UserPublicSchema(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        message="Login successful"
    )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserPublicSchema)
async def route_create_user(user: CreateUserSchema, session: Session = Depends(get_session)):
    '''
    Endpoint para criação de um novo usuário.
    Args:
        user (CreateUserSchema): Dados do usuário a ser criado.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.
    Returns:
        UserPublicSchema: O usuário criado com sucesso.
    '''
    try:
        new_user = create_user(session, user)
        return UserPublicSchema(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            role=new_user.role,
            created_at=new_user.created_at,
            message="User created successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )
    except SystemError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.patch('/', status_code=status.HTTP_200_OK, response_model=UserPublicSchema)
async def route_update_user(user_data: UpdateUserSchema, session: Session = Depends(get_session)):
    '''
    Endpoint para atualização dos dados de um usuário existente.
    Args:
        user_data (UpdateUserSchema): Os dados atualizados do usuário.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.
    Returns:
        UserPublicSchema: O usuário atualizado com sucesso.
    '''
    try:
        updated_user = update_user(session, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserPublicSchema(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            role=updated_user.role,
            created_at=updated_user.created_at,
            message="User updated successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating user: {str(e)}"
        )
    except SystemError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )
