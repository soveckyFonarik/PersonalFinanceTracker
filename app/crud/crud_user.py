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
    """
    CRUD операции для User с дополнительными методами.
    """

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """
        Получить пользователя по email.

        Args:
            db: Сессия БД
            email: Email пользователя

        Returns:
            Пользователь или None
        """
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(
        self, db: AsyncSession, *, username: str
    ) -> Optional[User]:
        """
        Получить пользователя по username.

        Args:
            db: Сессия БД
            username: Имя пользователя

        Returns:
            Пользователь или None
        """
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        Создать пользователя с проверкой уникальности.

        Args:
            db: Сессия БД
            obj_in: Данные пользователя

        Returns:
            Созданный пользователь

        Raises:
            ValueError: Если email или username уже существуют
        """
        # Проверяем уникальность email
        existing_email = await self.get_by_email(db, email=obj_in.email)
        if existing_email:
            raise ValueError("Пользователь с таким email уже существует")

        # Проверяем уникальность username
        existing_username = await self.get_by_username(db, username=obj_in.username)
        if existing_username:
            raise ValueError("Пользователь с таким username уже существует")

        # Создаем пользователя через родительский метод
        return await super().create(db, obj_in=obj_in)


# Создаем экземпляр для использования
user = CRUDUser(User)
