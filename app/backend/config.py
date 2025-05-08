from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Параметры конфигурации API, берутся с .env файла"""

    database: str
    hash_algo: str = "HS256"
    secret_key: str
    access_token_ttl_minutes: int = 60
    refresh_token_ttl_minutes: int = 60*120

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', case_sensitive=False)


config = Config()
