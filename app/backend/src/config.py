from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://echocad_admin:echocad_admin_password@localhost:3306/echocad_db?charset=utf8mb4"
    LOG_LEVEL: str = "INFO"
    jwt_secret_key: str = Field(
        alias="JWT_TOKEN", default="super_secret_jwt_key_change_me"
    )
    echo_database: bool = True
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    GROQ_API_KEY: str = Field(default="gsk_REPLACE_ME")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf_8", extra="ignore"
    )


settings = Settings()
logger.debug(settings.model_dump_json(indent=2))
