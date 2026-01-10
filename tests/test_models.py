"""
Тесты моделей SQLAlchemy.
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.models import Base
from app.models.note import Note
from app.models.category import Category
from app.models.user import User


class TestNoteModel:
    """Тесты модели Note."""

    def test_note_creation_in_memory(self):
        """Тест создания объекта Note в памяти."""
        note = Note(title="Тест", content="Описание")

        # ID может быть None пока объект не сохранен в БД
        # Это нормально для SQLAlchemy
        assert note.title == "Тест"
        assert note.content == "Описание"
        # created_at и updated_at тоже могут быть None до сохранения
        # assert note.created_at is None или assert isinstance(note.created_at, datetime)

    def test_note_with_explicit_id(self):
        """Тест создания Note с явным ID."""
        test_id = str(uuid.uuid4())
        note = Note(id=test_id, title="Тест с ID", content="Описание")

        assert note.id == test_id
        assert note.title == "Тест с ID"

    def test_note_repr(self):
        """Тест строкового представления."""
        note = Note(title="Тестовая заметка", content="Описание")
        repr_str = repr(note)

        assert "Note" in repr_str
        assert "title='Тестовая заметка'" in repr_str or "Тестовая заметка" in repr_str


class TestCategoryModel:
    """Тесты модели Category."""

    def test_category_creation_in_memory(self):
        """Тест создания объекта Category в памяти."""
        category = Category(name="Еда", color="#FF5733")

        # В памяти ID может быть None
        assert category.name == "Еда"
        assert category.color == "#FF5733"

    def test_category_with_explicit_id(self):
        """Тест создания Category с явным ID."""
        test_id = str(uuid.uuid4())
        category = Category(id=test_id, name="Еда", color="#FF5733")

        assert category.id == test_id
        assert category.name == "Еда"


class TestUserModel:
    """Тесты модели User."""

    def test_user_creation_in_memory(self):
        """Тест создания объекта User в памяти."""
        user = User(email="test@example.com", username="test_user")

        assert user.email == "test@example.com"
        assert user.username == "test_user"

    def test_user_with_explicit_id(self):
        """Тест создания User с явным ID."""
        test_id = str(uuid.uuid4())
        user = User(id=test_id, email="test@example.com", username="test_user")

        assert user.id == test_id
        assert user.email == "test@example.com"


@pytest.mark.asyncio
class TestDatabaseOperations:
    """Тесты операций с базой данных."""

    @pytest.mark.asyncio
    async def test_create_note_in_db_manual_session(self):
        """Тест сохранения Note в БД с ручным созданием сессии."""
        # Создаем engine и сессию
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

        # Создаем таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Создаем фабрику сессий
        AsyncSessionLocal = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        async with AsyncSessionLocal() as db_session:
            # Теперь создаем и тестируем Note
            note = Note(title="Тест БД", content="Описание")

            db_session.add(note)
            await db_session.flush()
            await db_session.refresh(note)

            # Проверки
            assert note.id is not None
            assert isinstance(note.id, str)
            assert len(note.id) == 36  # UUID

            assert note.created_at is not None
            assert note.updated_at is not None
            assert isinstance(note.created_at, datetime)
            assert isinstance(note.updated_at, datetime)

            # Проверяем получение из БД
            from_db = await db_session.get(Note, note.id)
            assert from_db is not None
            assert from_db.title == "Тест БД"
            assert from_db.content == "Описание"

            await db_session.commit()

        # Очистка таблиц
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        # Закрываем engine
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_create_note_in_db(self):
        """Тест сохранения Note в БД (аналогичный предыдущему, но с фикстурой)."""
        # Создаем engine
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

        # Создаем таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Создаем фабрику сессий
        AsyncSessionLocal = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

        # Создаем сессию
        async with AsyncSessionLocal() as db_session:
            note = Note(title="Тест БД", content="Описание")

            db_session.add(note)
            await db_session.flush()
            await db_session.refresh(note)

            # Теперь ID должен быть
            assert note.id is not None
            assert isinstance(note.id, str)
            assert len(note.id) == 36  # UUID длина

            # Даты тоже должны быть установлены
            assert note.created_at is not None
            assert note.updated_at is not None
            assert isinstance(note.created_at, datetime)
            assert isinstance(note.updated_at, datetime)

            # Проверяем что можно получить из БД
            from_db = await db_session.get(Note, note.id)
            assert from_db is not None
            assert from_db.title == "Тест БД"
            assert from_db.content == "Описание"

            await db_session.commit()

        # Очистка
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()

    @pytest.mark.asyncio
    async def test_create_category_in_db(self):
        """Тест сохранения Category в БД."""
        # Создаем engine
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

        # Создаем таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Создаем фабрику сессий
        AsyncSessionLocal = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

        async with AsyncSessionLocal() as db_session:
            category = Category(name="Тестовая категория", color="#FF5733")

            db_session.add(category)
            await db_session.flush()
            await db_session.refresh(category)

            assert category.id is not None
            assert category.created_at is not None
            assert category.updated_at is not None

            from_db = await db_session.get(Category, category.id)
            assert from_db is not None
            assert from_db.name == "Тестовая категория"
            assert from_db.color == "#FF5733"

            await db_session.commit()

        # Очистка
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()

    @pytest.mark.asyncio
    async def test_create_user_in_db(self):
        """Тест сохранения User в БД."""
        # Создаем engine
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

        # Создаем таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Создаем фабрику сессий
        AsyncSessionLocal = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

        async with AsyncSessionLocal() as db_session:
            user = User(email="test@example.com", username="test_user")

            db_session.add(user)
            await db_session.flush()
            await db_session.refresh(user)

            assert user.id is not None
            assert user.email == "test@example.com"
            assert user.username == "test_user"

            from_db = await db_session.get(User, user.id)
            assert from_db is not None
            assert from_db.email == "test@example.com"
            assert from_db.username == "test_user"

            await db_session.commit()

        # Очистка
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()
