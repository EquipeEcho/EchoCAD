from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://echocad_admin:echocad_admin_password@localhost:3306/echocad_db?charset=utf8mb4"
    DATABASE_ASYNC_URL: str = "mysql+aiomysql://echocad_admin:echocad_admin_password@localhost:3306/echocad_db?charset=utf8mb4"
    LOG_LEVEL: str = "INFO"
    jwt_secret_key: str = Field(
        alias="JWT_TOKEN", default="super_secret_jwt_key_change_me"
    )
    echo_database: bool = True
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    GROQ_API_KEY: str = Field(default="")
    SINAPI_UPLOAD_DIR: str = "./sinapi"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf_8", extra="ignore"
    )


settings = Settings()
safe_settings = settings.model_dump()
for secret_key in ("jwt_secret_key", "GROQ_API_KEY"):
    if safe_settings.get(secret_key):
        safe_settings[secret_key] = "***"
logger.debug(safe_settings)
