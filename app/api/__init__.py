# app/api/__init__.py
"""
Основной роутер API.
Здесь объединяем все endpoints роутеры.
"""

from fastapi import APIRouter

from app.api.endpoints import notes, categories

# Создаем основной роутер API
api_router = APIRouter()

# Включаем роутеры для разных ресурсов
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
