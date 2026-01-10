"""
Инициализация CRUD модуля.
"""

from app.crud.crud_note import note
from app.crud.crud_category import category
from app.crud.crud_user import user

__all__ = ["note", "category", "user"]
