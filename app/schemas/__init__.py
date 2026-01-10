"""
Пакет Pydantic схем.
Импортируем все схемы для удобного доступа.
"""

from app.schemas.note import Note, NoteCreate, NoteUpdate
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.schemas.user import User, UserCreate, UserUpdate  # ← Добавь когда создашь

__all__ = [
    # Note schemas
    "Note",
    "NoteCreate",
    "NoteUpdate",
    # Category schemas
    "Category",
    "CategoryCreate",
    "CategoryUpdate",
    # User schemas (добавь когда создашь)
    "User",
    "UserCreate",
    "UserUpdate",
]
