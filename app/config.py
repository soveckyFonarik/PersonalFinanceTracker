# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения."""

    ENVIRONMENT: str = "development"
    # Настройки PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "finance_tracker"

    # Настройки приложения
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # Настройки безопасности
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def database_url(self) -> str:
        """Возвращает URL для подключения к PostgreSQL через asyncpg"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Для разработки можно использовать SQLite
    @property
    def sqlite_url(self) -> str:
        """URL для SQLite (для разработки и тестов)"""
        return "sqlite+aiosqlite:///./finance.db"

    class Config:
        # Указываем файл .env для загрузки переменных окружения
        env_file = ".env"
        env_file_encoding = "utf-8"
        # case_sensitive = False
        extra = "ignore"  # Игнорировать лишние поля в .env


settings = Settings()
