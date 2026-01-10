from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class Note(BaseModel):
    """
    Модель для заметок (расходов/доходов).

    Таблица: notes
    Поля:
    - id, created_at, updated_at (из BaseModel)
    - title: заголовок заметки
    - content: описание/комментарий
    """

    __tablename__ = "notes"  # Имя таблицы в БД

    # Заголовок заметки
    title: Mapped[str] = mapped_column(
        String(100),  # Максимум 100 символов
        nullable=False,  # Обязательное поле
        index=True,  # Индекс для поиска по заголовку
    )

    # Содержимое заметки
    content: Mapped[str] = mapped_column(
        Text,  # Текст без ограничения длины
        nullable=True,  # Может быть пустым
        default=None,  # Значение по умолчанию
    )

    def __repr__(self) -> str:
        """Более информативное строковое представление"""
        return f"<Note(id={self.id}, title='{self.title[:20]}...')>"
