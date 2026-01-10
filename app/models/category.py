import re
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates
from app.models.base import BaseModel


class Category(BaseModel):
    """
    Модель для категорий расходов.

    Таблица: categories
    Поля:
    - id, created_at, updated_at (из BaseModel)
    - name: название категории (уникальное)
    - color: цвет в формате hex (#RRGGBB)
    """

    __tablename__ = "categories"

    # Название категории
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,  # Уникальное значение (не может быть двух одинаковых)
        index=True,
    )

    # Цвет категории (для UI)
    color: Mapped[str] = mapped_column(
        String(7),  # #RRGGBB (7 символов)
        nullable=False,
        default="#000000",  # Черный по умолчанию
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"

    @validates("color")
    def validate_color(self, key: str, color: str) -> str:
        """
        Валидация цвета перед сохранением в БД.
        Вызывается автоматически SQLAlchemy при установке значения.

        Проверяет формат hex цвета: #RRGGBB
        Примеры валидных значений: #FF5733, #000000, #FFFFFF
        """
        if not re.match(r"^#[0-9A-Fa-f]{6}$", color):
            raise ValueError(
                f"Некорректный формат цвета: {color}. "
                "Используйте hex формат: #RRGGBB"
            )
        return color

    @classmethod
    def is_valid_color(cls, color: str) -> bool:
        """Проверяет, является ли цвет валидным hex"""
        return bool(re.match(r"^#[0-9A-Fa-f]{6}$", color))
