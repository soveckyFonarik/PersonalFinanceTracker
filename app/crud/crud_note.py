"""
CRUD операции для заметок.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    """CRUD операции для заметок."""

    async def get_by_title(self, db: AsyncSession, *, title: str) -> Optional[Note]:
        """
        Получить заметку по заголовку.

        Args:
            db: Асинхронная сессия БД
            title: Заголовок заметки

        Returns:
            Заметка или None
        """
        result = await db.execute(select(Note).where(Note.title == title))
        return result.scalar_one_or_none()

    async def search(
        self, db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100
    ):
        """
        Поиск заметок по содержанию.

        Args:
            db: Асинхронная сессия БД
            query: Поисковый запрос
            skip: Сколько записей пропустить
            limit: Максимальное количество записей

        Returns:
            Список заметок
        """
        result = await db.execute(
            select(Note)
            .where(Note.title.ilike(f"%{query}%") | Note.content.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


# Создаем экземпляр CRUDNote для использования в приложении
note = CRUDNote(Note)
