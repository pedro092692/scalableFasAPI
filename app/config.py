from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = 'My FASTAPI app :)'
    app_env: str = 'development'
    app_debug: bool = False
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
