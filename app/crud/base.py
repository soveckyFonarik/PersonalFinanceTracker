"""
Базовый класс для CRUD операций.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Импортируем Base из ваших моделей
from app.models.base import BaseModel as AppBaseModel

# Типы для дженериков
# Используем AppBaseModel вместо Base, так как он имеет поле id
ModelType = TypeVar("ModelType", bound=AppBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс с CRUD операциями: Create, Read, Update, Delete.

    Generic параметры:
    - ModelType: SQLAlchemy модель (Note, Category, User)
    - CreateSchemaType: Pydantic схема для создания
    - UpdateSchemaType: Pydantic схема для обновления
    """

    def __init__(self, model: Type[ModelType]):
        """
        Инициализация CRUD с указанием модели.

        Args:
            model: SQLAlchemy модель
        """
        self.model = model

    async def get(self, db: AsyncSession, id: str) -> Optional[ModelType]:
        """
        Получить один объект по ID.

        Args:
            db: Сессия БД
            id: ID объекта (строка, UUID)

        Returns:
            Объект модели или None если не найден
        """
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Получить несколько объектов с пагинацией.

        Args:
            db: Сессия БД
            skip: Сколько пропустить
            limit: Максимальное количество

        Returns:
            Список объектов
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Создать новый объект.

        Args:
            db: Сессия БД
            obj_in: Данные для создания (Pydantic схема)

        Returns:
            Созданный объект
        """
        # Конвертируем Pydantic объект в dict
        obj_in_data = jsonable_encoder(obj_in)

        # Создаем объект модели
        db_obj = self.model(**obj_in_data)

        # Сохраняем в БД
        db.add(db_obj)
        await db.commit()
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
            db: Сессия БД
            db_obj: Существующий объект из БД
            obj_in: Данные для обновления (схема или dict)

        Returns:
            Обновленный объект
        """
        # Получаем данные для обновления
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # Обновляем поля объекта
        for field, value in update_data.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)

        # Сохраняем изменения
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def remove(self, db: AsyncSession, *, id: str) -> Optional[ModelType]:
        """
        Удалить объект по ID.

        Args:
            db: Сессия БД
            id: ID объекта для удаления (строка, UUID)

        Returns:
            Удаленный объект или None если не найден
        """
        # Получаем объект
        obj = await self.get(db, id)

        if obj:
            # Удаляем
            await db.delete(obj)
            await db.commit()

        return obj
