"""
Базовый класс для CRUD операций.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс CRUD с методами Create, Read, Update, Delete."""

    def __init__(self, model: Type[ModelType]):
        """
        Инициализация CRUD класса.

        Args:
            model: SQLAlchemy модель
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Union[str, UUID]) -> Optional[ModelType]:
        """
        Получить объект по ID.

        Args:
            db: Асинхронная сессия БД
            id: ID объекта

        Returns:
            Объект модели или None
        """
        from sqlalchemy import select, inspect

        mapper = inspect(self.model)

        # Используем primary_key из mapper
        stmt = select(self.model).where(mapper.primary_key[0] == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Получить список объектов с пагинацией.

        Args:
            db: Асинхронная сессия БД
            skip: Сколько записей пропустить
            limit: Максимальное количество записей

        Returns:
            Список объектов
        """
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Создать новый объект.

        Args:
            db: Асинхронная сессия БД
            obj_in: Pydantic схема с данными

        Returns:
            Созданный объект
        """
        # Преобразуем Pydantic модель в словарь
        obj_in_data = obj_in.model_dump()

        # Создаем объект SQLAlchemy
        db_obj = self.model(**obj_in_data)

        # Добавляем в сессию
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Обновить существующий объект.

        Args:
            db: Асинхронная сессия БД
            db_obj: Существующий объект из БД
            obj_in: Pydantic схема или словарь с данными для обновления

        Returns:
            Обновленный объект
        """
        # Если obj_in - Pydantic модель, преобразуем в словарь
        if isinstance(obj_in, BaseModel):
            update_data = obj_in.model_dump(exclude_unset=True)
        else:
            update_data = obj_in

        # Обновляем поля объекта
        for field in update_data:
            if hasattr(db_obj, field) and update_data[field] is not None:
                setattr(db_obj, field, update_data[field])

        # # Обновляем updated_at
        # if hasattr(db_obj, "updated_at"):
        #     from datetime import datetime

        #     db_obj.updated_at = datetime.utcnow()

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)

        return db_obj

    async def delete(
        self, db: AsyncSession, *, id: Union[str, UUID]
    ) -> Optional[ModelType]:
        """
        Удалить объект по ID.

        Args:
            db: Асинхронная сессия БД
            id: ID объекта для удаления

        Returns:
            Удаленный объект или None
        """
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.flush()
        return obj
