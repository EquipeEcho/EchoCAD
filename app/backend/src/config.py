from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # O Pydantic buscará por 'APP_DATABASE_URL' no ambiente
    database_url: str = 'mysql+pymysql://root:aaaa@localhost:3306/echocad_sql'
    debug: bool = False
    groq_api_key: str = ''  # Chave de API para Groq, se aplicável

    model_config = SettingsConfigDict(
        env_file='.env',              # Carrega variáveis de um arquivo .env
        env_file_encoding='utf-8',
        extra='allow'
    )

settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump_json(indent=2))
