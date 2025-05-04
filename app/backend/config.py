from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database: str
    hash_algo: str = "HS256"
    secret_key: str
    token_ttl_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', case_sensitive=False)


config = Config()
