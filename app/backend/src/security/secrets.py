import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from src.config import settings


def _get_fernet() -> Fernet:
    digest = hashlib.sha256(settings.jwt_secret_key.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_secret(value: str) -> str:
    return _get_fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_secret(value: str | None) -> str | None:
    if not value:
        return None

    try:
        return _get_fernet().decrypt(value.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        return None


def mask_secret(value: str | None) -> str | None:
    if not value:
        return None

    if len(value) <= 8:
        return f"{value[:2]}******"

    return f"{value[:4]}..."
