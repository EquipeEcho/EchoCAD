from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.config import settings
from src.controller.crud_users import get_user_by_id
from src.database import get_session
from src.models.projeto_db import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expires = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_expire_minutes))
    payload = {"sub": str(subject), "exp": expires}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception

    user = get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    return user
