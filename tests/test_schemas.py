"""
Тесты Pydantic схем.
"""

import pytest
from datetime import datetime
from app.schemas.note import NoteCreate, NoteUpdate, Note
from app.schemas.category import CategoryCreate, CategoryUpdate, Category
from app.schemas.user import UserCreate, UserUpdate, User


class TestNoteSchemas:
    """Тесты схем для Note."""

    def test_note_create_valid(self):
        """Тест валидного создания Note."""
        data = {"title": "Тестовая заметка", "content": "Описание заметки"}

        note = NoteCreate(**data)

        assert note.title == "Тестовая заметка"
        assert note.content == "Описание заметки"

    def test_note_create_invalid(self):
        """Тест невалидного создания Note."""
        # Слишком длинный заголовок
        with pytest.raises(ValueError) as exc_info:
            NoteCreate(title="A" * 200, content="Тест")

        error_str = str(exc_info.value)
        # Проверяем что ошибка связана с длиной строки
        assert "100 characters" in error_str or "string_too_long" in error_str

    def test_note_update_partial(self):
        """Тест частичного обновления Note."""
        note = NoteUpdate(title="Новый заголовок")

        assert note.title == "Новый заголовок"
        assert note.content is None

    def test_note_from_attributes(self):
        """Тест создания схемы из SQLAlchemy модели."""
        from app.models.note import Note as NoteModel

        model = NoteModel(
            id="test-uuid",
            title="Тест",
            content="Описание",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        schema = Note.model_validate(model)

        assert schema.id == "test-uuid"
        assert schema.title == "Тест"


class TestCategorySchemas:
    """Тесты схем для Category."""

    def test_category_create_valid(self):
        """Тест валидного создания Category."""
        category = CategoryCreate(name="Еда", color="#FF5733")

        assert category.name == "Еда"
        assert category.color == "#FF5733"

    def test_category_create_invalid_color(self):
        """Тест невалидного цвета."""
        with pytest.raises(ValueError) as exc_info:
            CategoryCreate(name="Еда", color="не hex")

        error_str = str(exc_info.value)
        # Проверяем что есть ошибка валидации
        assert "validation" in error_str.lower() or "invalid" in error_str.lower()

    def test_category_update_with_color(self):
        """Тест обновления с цветом."""
        category = CategoryUpdate(color="#000000")
        assert category.color == "#000000"

    def test_category_update_no_color(self):
        """Тест обновления без цвета."""
        category = CategoryUpdate(name="Новое имя")
        assert category.name == "Новое имя"
        assert category.color is None


class TestUserSchemas:
    """Тесты схем для User."""

    def test_user_create_valid(self):
        """Тест валидного создания User."""
        user = UserCreate(email="test@example.com", username="test_user")

        assert user.email == "test@example.com"
        assert user.username == "test_user"

    def test_user_create_invalid_email(self):
        """Тест невалидного email."""
        with pytest.raises(ValueError) as exc_info:
            UserCreate(email="not-an-email", username="test_user")

        error_str = str(exc_info.value)
        # Проверяем что есть ошибка валидации email
        assert "email" in error_str.lower() or "validation" in error_str.lower()

    def test_user_update_partial(self):
        """Тест частичного обновления User."""
        user = UserUpdate(username="new_username")

        assert user.username == "new_username"
        assert user.email is None

    def test_user_update_valid_email(self):
        """Тест обновления с валидным email."""
        user = UserUpdate(email="new@example.com")
        assert user.email == "new@example.com"
