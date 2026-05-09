import bcrypt

from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.projeto_db import User
from src.schemas.user_schema import CreateUser


def create_user(db: Session, user_schema: CreateUser) -> User:
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
    except Exception as e:
        db.rollback()
        raise e


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
        raise e
