# tests/conftest.py
"""
Общие фикстуры для тестов.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.models.base import Base


# Фикстура для тестовой базы данных в памяти
@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Создаем тестовую БД в памяти."""
    test_db_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(
        test_db_url,
        echo=False,
        future=True,
    )

    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Очищаем после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    """Сессия для тестовой БД."""
    AsyncTestSessionLocal = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncTestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@pytest_asyncio.fixture
async def client():
    """HTTP клиент для тестирования API."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# Автоматически переопределяем настройки для тестов
@pytest.fixture(autouse=True)
def override_settings():
    """
    Переопределяем настройки для тестов.
    """
    original_debug = settings.DEBUG
    original_db_url = settings.database_url_to_use

    # Включаем DEBUG для тестов
    settings.DEBUG = True

    yield

    # Восстанавливаем оригинальные настройки
    # settings.DEBUG = original_debug
    # settings.DATABASE_URL = original_db_url
