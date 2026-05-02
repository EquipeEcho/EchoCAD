from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://user:password@localhost:3306/test_db?charset=utf8mb4"
    main_model: str = 'qwen2.5:7b'
    agent_model: str = 'qwen2.5:3b'
    fast_model: str = 'qwen2.5:1.5b'
    model_options: dict[str, int | float] = {"temperature": 0.2}
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump_json(indent=4))
