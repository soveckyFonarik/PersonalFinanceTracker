from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""

    pass


# Создаем движок для подключения
engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Показывать SQL запросы в консоли при DEBUG=true
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency для получения сессии БД в FastAPI.

    Использование в FastAPI:
    @app.get("/items/")
    async def read_items(db: AsyncSession = Depends(get_db)):
        # работа с db
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


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
