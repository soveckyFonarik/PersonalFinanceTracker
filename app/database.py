from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


# class Base(DeclarativeBase):
#     """Базовый класс для всех моделей SQLAlchemy"""

#     pass

# Используем SQLite для разработки, PostgreSQL для продакшена
DATABASE_URL = settings.database_url if not settings.DEBUG else settings.sqlite_url

# Создаем движок для подключения
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # Показывать SQL запросы в консоли при DEBUG=true
    future=True,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,  # Пересоздание соединений каждый час
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Создаем объект database для удобного доступа в скриптах
class Database:
    """Класс для удобной работы с базой данных в скриптах"""

    def __init__(self):
        self.engine = engine
        self.session_factory = AsyncSessionLocal

    async def get_session(self) -> AsyncSession:
        """Получить сессию БД (альтернатива get_db для скриптов)"""
        return AsyncSessionLocal()

    async def connect(self):
        """Проверить подключение к БД"""
        async with self.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    async def disconnect(self):
        """Закрыть соединения с БД"""
        await self.engine.dispose()


# Создаем глобальный экземпляр для использования в скриптах
database = Database()
