from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field


app = FastAPI(
    title="Finance Tracker API",
    description="Person finance management API",
    version="0.1.0",
)


# Pydantic models
class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: Optional[str] = Field(None, max_length=1000)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, max_length=1000)


class Note(NoteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# db in memory
notes_db: List[Note] = []

# end points


@app.get("/")
async def root():
    return {"message": "Welcome to Finance Tracker API"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteCreate):
    """create new note"""
    new_note = Note(
        id=uuid4(),
        title=note.title,
        content=note.content,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    notes_db.append(new_note)
    return new_note


@app.get("/notes/", response_model=List[Note])
async def read_notes(skip: int = 0, limit: int = 10):
    """get list notes + pagination"""
    return notes_db[skip : skip + limit]


@app.get("/notes/{notes_id}", response_model=Note)
async def read_note(notes_id: UUID):
    for note in notes_db:
        if note.id == notes_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: UUID, note_update: NoteUpdate):
    """Обновить заметку"""
    for idx, note in enumerate(notes_db):
        if note.id == note_id:
            update_data = note_update.model_dump(exclude_unset=True)
            updated_note = note.model_copy(update=update_data)
            updated_note.updated_at = datetime.now(timezone.utc)
            notes_db[idx] = updated_note
            return updated_note
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}")
async def delete_note(note_id: UUID):
    """Удалить заметку"""
    for idx, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(idx)
            return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=404, detail="Note not found")
