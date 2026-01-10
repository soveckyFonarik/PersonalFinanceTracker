"""
Фикстуры для тестов.
"""

import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.config import settings


# Тестовая база данных (SQLite in-memory)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Движок для тестов
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=StaticPool,  # Для тестов используем статический пул
    connect_args={"check_same_thread": False},
)

# Сессия для тестов
TestAsyncSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Создаем event loop для тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Создает и удаляет таблицы для тестов."""
    # Создаем таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Удаляем таблицы после тестов
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для получения сессии БД."""
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
def override_get_db(db_session: AsyncSession):
    """Фикстура для подмены зависимости get_db."""

    async def _override_get_db():
        yield db_session

    return _override_get_db


def pytest_configure(config):
    """Регистрируем маркеры."""
    config.addinivalue_line("markers", "unit: unit tests (без БД)")
    config.addinivalue_line("markers", "integration: integration tests (с БД)")
    config.addinivalue_line("markers", "db: tests requiring database")
