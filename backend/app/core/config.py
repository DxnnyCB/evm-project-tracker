from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/evm_tracker"


class Settings(BaseSettings):
    """Configuración de la aplicación, cargada desde variables de entorno o .env."""

    database_url: str = DEFAULT_DATABASE_URL

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
