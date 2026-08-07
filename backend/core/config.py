from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "PDF Chatbot API"

    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    STORAGE_PROVIDER: str = "local"
    UPLOAD_DIR: str = "uploads"

    QDRANT_URL: str
    QDRANT_COLLECTION: str = "documents"

    GOOGLE_API_KEY: str

    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()