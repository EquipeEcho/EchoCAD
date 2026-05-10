import bcrypt

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.projeto_db import User
from src.schemas.user_schema import CreateUserSchema


def create_user(db: Session, user_schema: CreateUserSchema) -> User:
    '''
    Cria um novo usuário no banco de dados.
    Args:
        db (Session): Sessão do banco de dados.
        user_schema (CreateUser): Esquema de criação de usuário contendo os dados necessários.
        Returns:
            User: O objeto do usuário persistido, incluindo IDs e timestamps gerados.
    '''
    try:
        new_user = User(**user_schema.model_dump())
        new_user.password = bcrypt.hashpw(
            new_user.password.encode('utf-8'),
            bcrypt.gensalt()).decode('utf-8')
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
        raise


def get_user_by_email(db: Session, email: str, password: str) -> User | None:
    '''
    Recupera um usuário do banco de dados com base no email e senha.
    Args:
        db (Session): Sessão do banco de dados.
        email (str): O email do usuário a ser recuperado.
        password (str): A senha do usuário.
    Returns:
        User: O objeto do usuário correspondente ao email fornecido, ou None se não
        encontrado ou se a senha não corresponder.
    '''
    try:
        stmt = select(User).where(User.email == email)
        result = db.execute(stmt).scalar_one_or_none()
        if result and bcrypt.checkpw(
                password.encode('utf-8'),
                result.password.encode('utf-8')):
            return result
        return None
    except Exception as e:
        logger.error("Unexpected error occurred: {}", e)
        raise


def update_user(db: Session, user_id: int, user_schema: CreateUserSchema) -> User | None:
    '''
    Atualiza um usuário existente no banco de dados.
    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): O ID do usuário a ser atualizado.
        user_schema (CreateUser): Esquema de criação de usuário contendo os dados atualizados.
    Returns:
        User: O objeto do usuário atualizado, ou None se o usuário não for encontrado.
    '''
    try:
        stmt = select(User).where(User.id == user_id)
        user = db.execute(stmt).scalar_one_or_none()
        if not user:
            return None
        for key, value in user_schema.model_dump().items():
            setattr(user, key, value)
        if 'password' in user_schema.model_dump():
            user.password = bcrypt.hashpw(
                user.password.encode('utf-8'),
                bcrypt.gensalt()).decode('utf-8')
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        logger.error("Unexpected error occurred: {}", e)
        raise