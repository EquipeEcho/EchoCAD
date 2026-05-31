from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.auth import create_access_token, get_current_user
from src.database import get_async_session
from src.schemas.user_schema import (
    AIProviderStatusSchema,
    AIProviderToggleSchema,
    ChangePasswordSchema,
    CreateUserSchema,
    GroqApiKeyStatusSchema,
    GroqApiKeyUpdateSchema,
    TokenResponseSchema,
    UpdateUserSchema,
    UserPublicSchema,
)
from src.controller.crud_users import (
    change_user_password,
    clear_user_groq_api_key,
    create_user,
    get_ai_provider_preference,
    get_masked_user_groq_api_key,
    get_user_by_email,
    set_ai_provider_preference,
    set_user_groq_api_key,
    update_user,
    validate_ollama_available,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=TokenResponseSchema
)
async def route_login(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
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
            email = str(body.get("email"))
            password = str(body.get("password"))
        elif (
            "application/x-www-form-urlencoded" in content_type
            or "multipart/form-data" in content_type
        ):
            body = await request.form()
            email = (
                str(body.get("email"))
                if body.get("email")
                else str(body.get("username"))
            )
            password = str(body.get("password"))
        else:
            # Tenta JSON por padrão
            body = await request.json()
            email = str(body.get("email"))
            password = str(body.get("password"))
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

    user = await get_user_by_email(session, email, password)
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
    user: CreateUserSchema, session: AsyncSession = Depends(get_async_session)
):
    """
    Endpoint para criação de um novo usuário.
    Args:
        user (CreateUserSchema): Dados do usuário a ser criado.
        session (AsyncSession): Sessão do banco de dados, injetada automaticamente pelo FastAPI.
    Returns:
        UserPublicSchema: O usuário criado com sucesso.
    """
    try:
        new_user = await create_user(session, user)
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
    session: AsyncSession = Depends(get_async_session),
):
    """
    Endpoint para atualização dos dados de um usuário existente.
    Args:
        user_data (UpdateUserSchema): Os dados atualizados do usuário.
        session (AsyncSession): Sessão do banco de dados, injetada automaticamente pelo FastAPI.
    Returns:
        UserPublicSchema: O usuário atualizado com sucesso.
    """
    if user_data.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é permitido alterar dados de outro usuário.",
        )
    try:
        updated_user = await update_user(session, user_data)
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


@router.patch(
    "/me/password", status_code=status.HTTP_200_OK, response_model=UserPublicSchema
)
async def route_change_password(
    password_data: ChangePasswordSchema,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        updated_user = await change_user_password(
            session,
            current_user.id,
            password_data.current_password,
            password_data.new_password,
        )
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
            message="Senha alterada com sucesso",
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SystemError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/me/groq-key", status_code=status.HTTP_200_OK, response_model=GroqApiKeyStatusSchema
)
async def route_get_groq_key_status(current_user=Depends(get_current_user)):
    masked_key = get_masked_user_groq_api_key(current_user)
    return GroqApiKeyStatusSchema(
        configured=bool(masked_key),
        masked_key=masked_key,
        message="Chave Groq configurada" if masked_key else "Chave Groq nao configurada",
    )


@router.put(
    "/me/groq-key", status_code=status.HTTP_200_OK, response_model=GroqApiKeyStatusSchema
)
async def route_set_groq_key(
    key_data: GroqApiKeyUpdateSchema,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        updated_user = await set_user_groq_api_key(
            session, current_user.id, key_data.api_key
        )
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return GroqApiKeyStatusSchema(
            configured=True,
            masked_key=get_masked_user_groq_api_key(updated_user),
            message="Chave Groq salva com sucesso",
        )
    except SystemError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete(
    "/me/groq-key", status_code=status.HTTP_200_OK, response_model=GroqApiKeyStatusSchema
)
async def route_clear_groq_key(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        updated_user = await clear_user_groq_api_key(session, current_user.id)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return GroqApiKeyStatusSchema(
            configured=False,
            masked_key=None,
            message="Chave Groq removida com sucesso",
        )
    except SystemError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# === AI PROVIDER ==== #

@router.get(
    "/me/ai-provider",
    status_code=status.HTTP_200_OK,
    response_model=AIProviderStatusSchema
)
async def route_get_ai_provider(
    current_user=Depends(get_current_user)
):
    """Retorna preferência de IA atual do usuário"""
    pref = await get_ai_provider_preference(current_user)
    
    provider = pref["provider"]
    configured = pref["groq_configured"] if provider == "groq" else await validate_ollama_available()
    
    return AIProviderStatusSchema(
        use_ollama=pref["use_ollama"],
        provider_name=provider,
        configured=configured,
        message=f"Usando {provider.upper()}"
    )


@router.put(
    "/me/ai-provider",
    status_code=status.HTTP_200_OK,
    response_model=AIProviderStatusSchema
)
async def route_set_ai_provider(
    toggle: AIProviderToggleSchema,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Salva preferência de IA do usuário"""
    
    # Se escolher Ollama, validar que está disponível
    if toggle.use_ollama:
        if not await validate_ollama_available():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Ollama não está acessível em {settings.OLLAMA_URL}"
            )
    
    updated_user = await set_ai_provider_preference(
        session, 
        current_user.id, 
        toggle.use_ollama
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    provider = "ollama" if toggle.use_ollama else "groq"
    
    return AIProviderStatusSchema(
        use_ollama=toggle.use_ollama,
        provider_name=provider,
        configured=True,
        message=f"Alterado para {provider.upper()}"
    )
