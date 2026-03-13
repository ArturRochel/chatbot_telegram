from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    REDIS_URL: str
    TELEGRAM_TOKEN: str
    WHATSAPP_API_URL: str
    WHATSAPP_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Evita que variáveis extras no .env causem erro
    )

@lru_cache()
def get_configs() -> Settings:
    return Settings()