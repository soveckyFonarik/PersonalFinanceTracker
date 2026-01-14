"""
Пакет Pydantic схем.
Импортируем все схемы для удобного доступа.
"""

from app.schemas.note import NoteSchema, NoteCreate, NoteUpdate, Note
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.schemas.user import User, UserCreate, UserUpdate

__all__ = [
    # Note schemas
    "Note",
    "NoteSchema",
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
