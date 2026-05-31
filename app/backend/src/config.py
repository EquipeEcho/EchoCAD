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
    
    # Groq Configuration
    GROQ_API_KEY: str = Field(default="")
    GROQ_MODEL: str = Field(default="llama-3.3-70b-versatile")
    GROQ_MAX_RETRIES: int = Field(default=5)
    GROQ_TIMEOUT_SECONDS: float = Field(default=100.0)
    
    # Ollama Configuration (NEW - v2.0)
    OLLAMA_URL: str = Field(default="http://localhost:11434")
    OLLAMA_MODEL: str = Field(default="qwen2.5:7b")
    OLLAMA_TIMEOUT_SECONDS: float = Field(default=120.0)

    # CORS
    CORS_ORIGINS: list[str] = Field(default=["http://localhost:5173", "http://localhost:3000"])

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf_8", extra="ignore"
    )
    
    @field_validator('OLLAMA_URL')
    @classmethod
    def validate_ollama_url(cls, v):
        """Garante que URL não tem trailing slash"""
        return v.rstrip('/') if v else v


settings = Settings()
safe_settings = settings.model_dump()
for secret_key in ("jwt_secret_key", "GROQ_API_KEY"):
    if safe_settings.get(secret_key):
        safe_settings[secret_key] = "***"
logger.debug(safe_settings)
