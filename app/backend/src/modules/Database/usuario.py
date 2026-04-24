from sqlalchemy.orm import Session
from src.models import User
from ...schemas.database.usuario import CreateUser


def create_usuario(db: Session, user: CreateUser):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def read_usuario(db: Session, usuario_id: int):
    return db.query(User).filter(User.ID == usuario_id).first()


def read_all_usuarios(db: Session):
    return db.query(User).all()
