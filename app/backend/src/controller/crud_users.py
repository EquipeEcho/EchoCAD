import bcrypt

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.projeto_db import User
from src.schemas.user_schema import CreateUserSchema, UpdateUserSchema


def create_user(db: Session, user_schema: CreateUserSchema) -> User:
    """
    Cria um novo usuário no banco de dados.
    Args:
        db (Session): Sessão do banco de dados.
        user_schema (CreateUser): Esquema de criação de usuário contendo os dados necessários.
    Returns:
        User: O objeto do usuário persistido, incluindo IDs e timestamps gerados.
    Raises:
        ValueError: Se já existir um usuário com o mesmo email.
        SystemError: Se ocorrer um erro inesperado durante a criação do usuário.
    """
    try:
        new_user = User(**user_schema.model_dump())
        new_user.password = bcrypt.hashpw(
            new_user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        logger.error("Error creating user: {}", e)
        raise ValueError("Já existe um usuário com este email") from e
    except Exception as e:
        db.rollback()
        logger.error("Unexpected error occurred: {}", e)
        raise SystemError(
            "Ocorreu um erro inesperado ao criar o usuário, "
            "para mais informações consulte o log"
        ) from e


def get_user_by_email(db: Session, email: str, password: str) -> User | None:
    """
    Recupera um usuário do banco de dados com base no email e senha.
    Args:
        db (Session): Sessão do banco de dados.
        email (str): O email do usuário a ser recuperado.
        password (str): A senha do usuário.
    Returns:
        User: O objeto do usuário correspondente ao email fornecido, ou None se não
        encontrado ou se a senha não corresponder.
    Raises:
        SystemError: Se ocorrer um erro inesperado durante a recuperação do usuário.
    """
    try:
        stmt = select(User).where(User.email == email)
        result = db.execute(stmt).scalar_one_or_none()
        if result and bcrypt.checkpw(
            password.encode("utf-8"), result.password.encode("utf-8")
        ):
            return result
        return None
    except Exception as e:
        logger.error("Unexpected error occurred: {}", e)
        raise SystemError("Ocorreu um erro inesperado ao recuperar o usuário") from e


def update_user(db: Session, user_schema: UpdateUserSchema) -> User | None:
    """
    Atualiza um usuário existente no banco de dados.
    Args:
        db (Session): Sessão do banco de dados.
        user_schema (UpdateUserSchema): Esquema de atualização de usuário contendo os dados atualizados.
    Returns:
        User: O objeto do usuário atualizado, ou None se o usuário não for encontrado.
    Raises:
        ValueError: Se a senha atual fornecida estiver incorreta.
        SystemError: Se ocorrer um erro inesperado durante a atualização do usuário.
    """
    try:
        stmt = select(User).where(User.id == user_schema.id)
        user = db.execute(stmt).scalar_one_or_none()

        if not user:
            return None

        if not bcrypt.checkpw(
            user_schema.password.encode("utf-8"), user.password.encode("utf-8")
        ):
            raise ValueError("Senha atual incorreta")

        for key, value in user_schema.model_dump(exclude_unset=True).items():
            if key == "password":
                continue
            if key == "new_password":
                hash_password = bcrypt.hashpw(
                    value.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                setattr(user, "password", hash_password)
                continue
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    except ValueError as e:
        db.rollback()
        logger.error("Error updating user: {}", e)
        raise ValueError(str(e)) from e
    except Exception as e:
        db.rollback()
        logger.error("Unexpected error occurred: {}", e)
        raise SystemError(
            "Ocorreu um erro inesperado ao atualizar o usuário, "
            "para mais informações consulte o log"
        ) from e
