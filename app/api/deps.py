# app/api/deps.py
"""
Зависимости (dependencies) для API endpoints.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения асинхронной сессии БД.

    Использование:
    @router.get("/")
    async def read_items(db: AsyncSession = Depends(get_db)):
        ...

    Yields:
        AsyncSession: Сессия базы данных
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
