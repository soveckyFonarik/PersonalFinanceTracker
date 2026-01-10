"""
CRUD операции для пользователей.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD операции для пользователей."""

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """
        Получить пользователя по email.

        Args:
            db: Асинхронная сессия БД
            email: Email пользователя

        Returns:
            Пользователь или None
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(
        self, db: AsyncSession, *, username: str
    ) -> Optional[User]:
        """
        Получить пользователя по username.

        Args:
            db: Асинхронная сессия БД
            username: Имя пользователя

        Returns:
            Пользователь или None
        """
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()


# Создаем экземпляр CRUDUser для использования в приложении
user = CRUDUser(User)
