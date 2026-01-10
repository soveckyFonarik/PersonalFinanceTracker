import os
from dotenv import load_dotenv

# from pydantic_settings import BaseSettings
# from typing import Optional
load_dotenv()


class Settings:
    """Настройки приложения из переменных окружения"""

    # Настройки PostgreSQL
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
    postgres_user = os.getenv("POSTGRES_USER", "postgres")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "")
    postgres_db = os.getenv("POSTGRES_DB", "finance_tracker")

    # Настройки приложения
    debug: bool = bool(os.getenv("DEBUG", False))
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")

    # Формируем URL для подключения
    @property
    def database_url(self) -> str:
        """Возвращает URL для подключения к PostgreSQL через asyncpg"""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


# Глобальный объект настроек
settings = Settings()
