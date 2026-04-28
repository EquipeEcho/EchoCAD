from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = 'mysql+pymysql://root:aaaa@localhost:3306/echocad_sql'
    main_model: str = 'qwen2.5:7b'
    model_options: dict[str, int | float] = {"temperature": 0.2}
    api_key: str = ''
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow'
    )


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump_json(indent=4))
