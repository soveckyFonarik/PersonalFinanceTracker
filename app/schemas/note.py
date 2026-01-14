from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class NoteBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Заголовок заметки (1-100 символов)",
        examples=["Продукты на неделю"],
    )

    content: Optional[str] = Field(
        default=None,  # ← ЕСТЬ default=None?
        max_length=1000,
        description="Текст заметки (до 1000 символов)",
        examples=["Купить молоко, хлеб, яйца"],
    )


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,  # ← ЕСТЬ default=None?
        min_length=1,
        max_length=100,
        description="Новый заголовок заметки",
    )

    content: Optional[str] = Field(
        default=None,  # ← ЕСТЬ default=None?
        max_length=1000,
        description="Новый текст заметки",
    )


class NoteSchema(NoteBase):
    id: str = Field(..., description="Уникальный идентификатор заметки")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    model_config = ConfigDict(from_attributes=True)


Note = NoteSchema

__all__ = ["NoteBase", "NoteCreate", "NoteUpdate", "NoteSchema", "Note"]
