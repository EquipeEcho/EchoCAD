from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://echocad_admin:echocad_admin_password@localhost:3306/echocad_db?charset=utf8mb4"
    log_level: str = "INFO"
    echo_database: bool = True
    jwt_secret_key: str = "super-secret-jwt-key-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
