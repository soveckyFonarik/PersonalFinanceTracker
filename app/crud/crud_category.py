"""
CRUD операции для категорий.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    """CRUD операции для категорий."""

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        """
        Получить категорию по имени.

        Args:
            db: Асинхронная сессия БД
            name: Имя категории

        Returns:
            Категория или None
        """
        result = await db.execute(select(Category).where(Category.name == name))
        return result.scalar_one_or_none()


# Создаем экземпляр CRUDCategory для использования в приложении
category = CRUDCategory(Category)
