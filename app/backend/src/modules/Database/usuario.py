from sqlalchemy.orm import Session
from src.models import Usuario
from ...schemas.database.usuario import CreateUser
import hashlib
import hmac
import secrets


def hash_password(password: str) -> str:
    """Gera hash PBKDF2-HMAC-SHA256 com salt aleatório."""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"{salt}${pwd_hash.hex()}"


def verify_password(password: str, stored_password: str) -> bool:
    """Valida senha em texto puro contra hash armazenado."""
    try:
        salt, stored_hash = stored_password.split("$", 1)
    except ValueError:
        return False

    candidate_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000).hex()
    return hmac.compare_digest(candidate_hash, stored_hash)


def create_usuario(db: Session, user: CreateUser):
    user_data = user.model_dump()
    user_data["senha"] = hash_password(user_data["senha"])
    new_user = Usuario(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def read_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def read_all_usuarios(db: Session):
    return db.query(Usuario).all()


def read_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def authenticate_usuario(db: Session, email: str, senha: str):
    user = read_usuario_by_email(db, email)
    if not user:
        return None

    if not verify_password(senha, user.senha):
        return None

    return user
