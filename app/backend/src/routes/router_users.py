from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from src.auth import create_access_token, get_current_user
from src.database import get_session
from src.schemas.user_schema import (
    CreateUserSchema,
    LoginUserSchema,
    TokenResponseSchema,
    UpdateUserSchema,
    UserPublicSchema,
)
from src.controller.crud_users import get_user_by_email, create_user, update_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=TokenResponseSchema
)
async def route_login(request: Request, session: Session = Depends(get_session)):
    """
    Endpoint para autenticação de usuários.
    Aceita tanto JSON quanto form-encoded data.
    """
    content_type = request.headers.get("content-type", "")
    email = None
    password = None

    try:
        if "application/json" in content_type:
            body = await request.json()
            email = body.get("email")
            password = body.get("password")
        elif (
            "application/x-www-form-urlencoded" in content_type
            or "multipart/form-data" in content_type
        ):
            body = await request.form()
            email = body.get("email") or body.get("username")
            password = body.get("password")
        else:
            # Tenta JSON por padrão
            body = await request.json()
            email = body.get("email")
            password = body.get("password")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar requisição: {str(e)}",
        )

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email/username e password são obrigatórios",
        )

    user = get_user_by_email(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id))
    response = TokenResponseSchema(
        access_token=access_token,
        token_type="bearer",
        user=UserPublicSchema(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            message="Login successful",
        ),
    )
    return response


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=TokenResponseSchema
)
async def route_create_user(
    user: CreateUserSchema, session: Session = Depends(get_session)
):
    """
    Endpoint para criação de um novo usuário.
    Args:
        user (CreateUserSchema): Dados do usuário a ser criado.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.
    Returns:
        UserPublicSchema: O usuário criado com sucesso.
    """
    try:
        new_user = create_user(session, user)
        access_token = create_access_token(subject=str(new_user.id))
        return TokenResponseSchema(
            access_token=access_token,
            token_type="bearer",
            user=UserPublicSchema(
                id=new_user.id,
                name=new_user.name,
                email=new_user.email,
                role=new_user.role,
                created_at=new_user.created_at,
                message="User created successfully",
            ),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}",
        )
    except SystemError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}",
        )


@router.patch("/", status_code=status.HTTP_200_OK, response_model=UserPublicSchema)
async def route_update_user(
    user_data: UpdateUserSchema,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Endpoint para atualização dos dados de um usuário existente.
    Args:
        user_data (UpdateUserSchema): Os dados atualizados do usuário.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.
    Returns:
        UserPublicSchema: O usuário atualizado com sucesso.
    """
    try:
        updated_user = update_user(session, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserPublicSchema(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            role=updated_user.role,
            created_at=updated_user.created_at,
            message="User updated successfully",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating user: {str(e)}",
        )
    except SystemError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}",
        )
