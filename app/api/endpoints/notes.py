# app/api/endpoints/notes.py
"""
API endpoints для работы с заметками.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

# from app import schemas
from app.api.deps import get_db
from app.crud import note as crud_note
from app.schemas.note import Note, NoteCreate, NoteUpdate

router = APIRouter()


@router.get("/", response_model=List[Note])
async def read_notes(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
) -> List[Note]:
    """
    Получить список заметок с пагинацией.

    Args:
        db: Сессия БД
        skip: Сколько записей пропустить
        limit: Максимальное количество записей

    Returns:
        Список заметок
    """
    notes = await crud_note.get_multi(db, skip=skip, limit=limit)
    return [Note.from_orm(note) for note in notes]


@router.get("/{note_id}", response_model=Note)
async def read_note(
    note_id: str,
    db: AsyncSession = Depends(get_db),
) -> Note:
    """
    Получить заметку по ID.

    Args:
        note_id: UUID заметки
        db: Сессия БД

    Returns:
        Заметка

    Raises:
        HTTPException: 404 если заметка не найдена
    """
    note = await crud_note.get(db, id=note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена"
        )
    return Note.from_orm(note)


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_in: NoteCreate,
    db: AsyncSession = Depends(get_db),
) -> Note:
    """
    Создать новую заметку.

    Args:
        note_in: Данные для создания заметки
        db: Сессия БД

    Returns:
        Созданная заметка
    """
    note = await crud_note.create(db, obj_in=note_in)
    return Note.from_orm(note)


@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: str,
    note_in: NoteUpdate,
    db: AsyncSession = Depends(get_db),
) -> Note:
    """
    Обновить заметку.

    Args:
        note_id: UUID заметки
        note_in: Данные для обновления
        db: Сессия БД

    Returns:
        Обновленная заметка

    Raises:
        HTTPException: 404 если заметка не найдена
    """
    note = await crud_note.get(db, id=note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена"
        )

    updated_note = await crud_note.update(db, db_obj=note, obj_in=note_in)
    return Note.from_orm(updated_note)


@router.delete("/{note_id}", response_model=Note)
async def delete_note(
    note_id: str,
    db: AsyncSession = Depends(get_db),
) -> Note:
    """
    Удалить заметку.

    Args:
        note_id: UUID заметки
        db: Сессия БД

    Returns:
        Удаленная заметка

    Raises:
        HTTPException: 404 если заметка не найдена
    """
    note = await crud_note.get(db, id=note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена"
        )

    deleted_note = await crud_note.remove(db, id=note_id)
    return Note.from_orm(deleted_note)
