# app/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Настройки приложения."""

    # =========== БАЗОВЫЕ НАСТРОЙКИ ===========
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # =========== ПРОЕКТ ===========
    PROJECT_NAME: str = "Personal Finance Tracker"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "API для управления личными финансами"

    # =========== API ===========
    API_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    # =========== БАЗА ДАННЫХ ===========
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "finance_tracker"

    # =========== БЕЗОПАСНОСТЬ ===========
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

    @property
    def sqlite_url(self) -> str:
        """URL для SQLite (для разработки и тестов)"""
        return "sqlite+aiosqlite:///./finance.db"

    @property
    def database_url_to_use(self) -> str:
        """Выбираем URL базы данных в зависимости от окружения"""
        if self.ENVIRONMENT == "development":
            return self.sqlite_url
        return self.database_url

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


# Создаем глобальный экземпляр настроек
settings = Settings()
