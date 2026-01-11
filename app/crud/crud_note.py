"""
CRUD операции для заметок.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    """
    CRUD операции для Note с дополнительными методами.
    """

    async def search_by_title(
        self, db: AsyncSession, *, title: str, skip: int = 0, limit: int = 100
    ) -> List[Note]:
        """
        Поиск заметок по заголовку (case-insensitive).

        Args:
            db: Сессия БД
            title: Часть заголовка для поиска
            skip: Сколько пропустить
            limit: Максимальное количество

        Returns:
            Список найденных заметок
        """
        query = (
            select(Note).where(Note.title.ilike(f"%{title}%")).offset(skip).limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_multi_by_user(
        self, db: AsyncSession, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Note]:
        """
        Получить заметки пользователя (заготовка на будущее).

        Args:
            db: Сессия БД
            user_id: ID пользователя
            skip: Сколько пропустить
            limit: Максимальное количество

        Returns:
            Список заметок пользователя
        """
        # Пока просто возвращаем все заметки
        # В будущем добавим связь Note -> User
        return await self.get_multi(db, skip=skip, limit=limit)


# Создаем экземпляр для использования
note = CRUDNote(Note)
