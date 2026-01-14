"""
Основной файл приложения FastAPI.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import api_router
from app.core.config import settings
from app.database import database, AsyncSessionLocal
from app.models.base import Base  # Импортируем Base из моделей


# =========== LIFESPAN МЕНЕДЖЕР ===========
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер для управления жизненным циклом приложения.
    Выполняется при старте и остановке приложения.
    """
    # Startup: инициализация БД
    print("🚀 Инициализация базы данных...")
    await init_database()

    yield

    # Shutdown: очистка ресурсов
    print("👋 Закрытие соединений с БД...")
    await database.disconnect()


# =========== ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ БД ===========
async def init_database():
    """Создание таблиц в базе данных, если они не существуют"""
    try:
        # Проверяем подключение
        await database.connect()
        print("✅ Подключение к БД успешно")

        # Создаем таблицы
        async with database.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("✅ Таблицы созданы/проверены")

        # await create_initial_data()

    except Exception as e:
        print(f"❌ Ошибка при инициализации БД: {e}")
        print("⚠️  Приложение запущено без БД. Проверьте подключение.")


async def create_initial_data():
    """Создание начальных данных (опционально)"""
    from app.models.category import Category
    from app.crud import category as crud_category

    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже категории
        categories = await session.execute(text("SELECT COUNT(*) FROM categories"))
        count = categories.scalar()

        if count == 0:
            print("📝 Создание начальных категорий...")

            initial_categories = [
                {"name": "Еда", "description": "Покупка продуктов"},
                {"name": "Транспорт", "description": "Транспортные расходы"},
                {"name": "Развлечения", "description": "Кино, рестораны, хобби"},
                {"name": "Здоровье", "description": "Медицина, спорт"},
                {"name": "Образование", "description": "Курсы, книги"},
            ]

            for cat_data in initial_categories:
                category = Category(**cat_data)
                session.add(category)

            await session.commit()
            print(f"✅ Создано {len(initial_categories)} категорий")


# =========== СОЗДАНИЕ ПРИЛОЖЕНИЯ ===========
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,  # Добавляем lifespan менеджер
)

# =========== CORS НАСТРОЙКИ ===========
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# =========== ПОДКЛЮЧЕНИЕ API РОУТЕРОВ ===========
app.include_router(api_router, prefix=settings.API_PREFIX)
