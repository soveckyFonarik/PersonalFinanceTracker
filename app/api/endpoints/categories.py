# app/api/endpoints/categories.py
"""
API endpoints для работы с категориями.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud import category as crud_category
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.get("/", response_model=List[Category])
async def read_categories(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
) -> List[Category]:
    """
    Получить список категорий.
    """
    categories = await crud_category.get_multi(db, skip=skip, limit=limit)
    return [Category.from_orm(category) for category in categories]


@router.get("/{category_id}", response_model=Category)
async def read_category(
    category_id: str,
    db: AsyncSession = Depends(get_db),
) -> Category:
    """
    Получить категорию по ID.
    """
    category = await crud_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )
    return Category.from_orm(category)


@router.get("/name/{category_name}", response_model=Optional[Category])
async def read_category_by_name(
    category_name: str,
    db: AsyncSession = Depends(get_db),
) -> Optional[Category]:
    """
    Получить категорию по имени.

    Returns:
        Категория или None если не найдена (не вызывает 404)
    """
    category = await crud_category.get_by_name(db, name=category_name)
    return Category.from_orm(category)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db),
) -> Category:
    """
    Создать новую категорию.
    """
    # Проверяем, нет ли уже категории с таким именем
    existing_category = await crud_category.get_by_name(db, name=category_in.name)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким именем уже существует",
        )

    category = await crud_category.create(db, obj_in=category_in)
    return Category.from_orm(category)


@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: str,
    category_in: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
) -> Category:
    """
    Обновить категорию.
    """
    category = await crud_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    # Если меняем имя, проверяем что оно уникально
    if category_in.name and category_in.name != category.name:
        existing_category = await crud_category.get_by_name(db, name=category_in.name)
        if existing_category and existing_category.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким именем уже существует",
            )

    updated_category = await crud_category.update(
        db, db_obj=category, obj_in=category_in
    )
    return Category.from_orm(updated_category)


@router.delete("/{category_id}", response_model=Category)
async def delete_category(
    category_id: str,
    db: AsyncSession = Depends(get_db),
) -> Category:
    """
    Удалить категорию.
    """
    category = await crud_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    deleted_category = await crud_category.remove(db, id=category_id)
    return Category.from_orm(deleted_category)
