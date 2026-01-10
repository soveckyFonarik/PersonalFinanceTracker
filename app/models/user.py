from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class User(BaseModel):
    """
    Модель для пользователей.

    Таблица: users
    Поля:
    - id, created_at, updated_at (из BaseModel)
    - email: email пользователя
    """

    __tablename__ = "users"  # Имя таблицы в БД

    # Заголовок заметки
    email: Mapped[str] = mapped_column(
        String(100),  # Максимум 100 символов
        nullable=False,  # Обязательное поле
        index=True,  # Индекс для поиска по заголовку
        unique=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),  # Максимум 50 символов
        nullable=False,  # Обязательное поле
        index=True,  # Индекс для поиска по заголовку
        unique=True,
    )

    def __repr__(self) -> str:
        """Более информативное строковое представление"""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email[:20]}...')>"
