from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # O Pydantic buscará por 'APP_DATABASE_URL' no ambiente
    database_url: str = 'mysql+pymysql://root:fatec@localhost:3306/echocad'
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',              # Carrega variáveis de um arquivo .env
        env_file_encoding='utf-8',
        extra='allow'
    )

settings = Settings()

if __name__ == "__main__":
    print("Configurações carregadas:")
    print(f"DATABASE_URL: {settings.database_url}")
    print(f"DEBUG: {settings.debug}")
