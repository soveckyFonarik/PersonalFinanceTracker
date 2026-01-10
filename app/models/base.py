import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, func, null
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    Все модели будут наследоваться от этого класса.
    """

    pass


class BaseModel(Base):
    """
    Абстрактная модель с общими полями для всех таблиц.

    Содержит поля, которые есть у ВСЕХ моделей:
    - id: уникальный идентификатор (UUID)
    - created_at: когда создана запись
    - updated_at: когда обновлена запись
    """

    __abstract__ = True
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """Строковое представление модели для отладки"""
        return f"<{self.__class__.__name__}(id={self.id})>"
