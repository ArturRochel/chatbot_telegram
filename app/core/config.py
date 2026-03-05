from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    REDIS_URL: str
    TELEGRAM_TOKEN: str
    TELEGRAM_API_URL: str
    WHATSAPP_API_URL: str
    WHATSAPP_TOKEN: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
    