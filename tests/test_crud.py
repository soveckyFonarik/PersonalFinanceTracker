"""
Тесты CRUD операций.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.models import Base
from app.crud import note, category, user
from app.schemas.note import NoteCreate, NoteUpdate
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.user import UserCreate, UserUpdate


@pytest.mark.asyncio
class TestCRUDNote:
    """Тесты CRUD операций для заметок."""

    @pytest.fixture(autouse=True)
    async def setup_db(self):
        """Настройка тестовой БД."""
        self.engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

        # Создаем таблицы
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Создаем фабрику сессий
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

        yield

        # Очищаем таблицы
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await self.engine.dispose()

    async def test_create_note(self):
        """Тест создания заметки."""
        async with self.AsyncSessionLocal() as db:
            note_in = NoteCreate(title="Тестовая заметка", content="Описание")
            note_obj = await note.create(db, obj_in=note_in)

            assert note_obj.id is not None
            assert note_obj.title == "Тестовая заметка"
            assert note_obj.content == "Описание"

            await db.commit()

    async def test_get_note(self):
        """Тест получения заметки по ID."""
        async with self.AsyncSessionLocal() as db:
            # Создаем заметку
            note_in = NoteCreate(title="Тест", content="Описание")
            note_obj = await note.create(db, obj_in=note_in)
            await db.commit()

            # Получаем заметку
            note_db = await note.get(db, id=note_obj.id)
            assert note_db is not None
            assert note_db.id == note_obj.id
            assert note_db.title == "Тест"

    async def test_update_note(self):
        """Тест обновления заметки."""
        async with self.AsyncSessionLocal() as db:
            # Создаем заметку
            note_in = NoteCreate(title="Старый заголовок", content="Старое описание")
            note_obj = await note.create(db, obj_in=note_in)
            await db.commit()

            # Обновляем заметку
            note_update = NoteUpdate(title="Новый заголовок")
            updated_note = await note.update(db, db_obj=note_obj, obj_in=note_update)

            assert updated_note.title == "Новый заголовок"
            assert updated_note.content == "Старое описание"  # Не изменилось
            assert updated_note.updated_at is not None

            await db.commit()

    async def test_delete_note(self):
        """Тест удаления заметки."""
        async with self.AsyncSessionLocal() as db:
            # Создаем заметку
            note_in = NoteCreate(title="Для удаления", content="Описание")
            note_obj = await note.create(db, obj_in=note_in)
            await db.commit()

            # Удаляем заметку
            deleted_note = await note.delete(db, id=note_obj.id)
            assert deleted_note is not None
            assert deleted_note.id == note_obj.id

            # Проверяем что заметка удалена
            note_db = await note.get(db, id=note_obj.id)
            assert note_db is None

            await db.commit()

    async def test_get_multi_notes(self):
        """Тест получения списка заметок."""
        async with self.AsyncSessionLocal() as db:
            # Создаем несколько заметок
            for i in range(5):
                note_in = NoteCreate(title=f"Заметка {i}", content=f"Описание {i}")
                await note.create(db, obj_in=note_in)

            await db.commit()

            # Получаем все заметки
            notes = await note.get_multi(db)
            assert len(notes) == 5

            # Проверяем пагинацию
            notes_limited = await note.get_multi(db, skip=2, limit=2)
            assert len(notes_limited) == 2

    async def test_search_notes(self):
        """Тест поиска заметок."""
        async with self.AsyncSessionLocal() as db:
            # Создаем заметки
            notes_data = [
                ("Python программирование", "Изучение Python"),
                ("Django фреймворк", "Веб-разработка на Django"),
                ("FastAPI приложение", "Создание API на FastAPI"),
            ]

            for title, content in notes_data:
                note_in = NoteCreate(title=title, content=content)
                await note.create(db, obj_in=note_in)

            await db.commit()

            # Ищем по заголовку
            python_notes = await note.search(db, query="Python")
            assert len(python_notes) == 1
            assert "Python" in python_notes[0].title

            # Ищем по содержанию
            api_notes = await note.search(db, query="API")
            assert len(api_notes) == 1
            assert "FastAPI" in api_notes[0].title


@pytest.mark.asyncio
class TestCRUDCategory:
    """Тесты CRUD операций для категорий."""

    @pytest.fixture(autouse=True)
    async def setup_db(self):
        """Настройка тестовой БД."""
        self.engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

        # Создаем таблицы
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Создаем фабрику сессий
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

        yield

        # Очищаем таблицы
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await self.engine.dispose()

    async def test_create_category(self):
        """Тест создания категории."""
        async with self.AsyncSessionLocal() as db:
            category_in = CategoryCreate(name="Еда", color="#FF5733")
            category_obj = await category.create(db, obj_in=category_in)

            assert category_obj.id is not None
            assert category_obj.name == "Еда"
            assert category_obj.color == "#FF5733"

            await db.commit()

    async def test_get_by_name_category(self):
        """Тест получения категории по имени."""
        async with self.AsyncSessionLocal() as db:
            # Создаем категорию
            category_in = CategoryCreate(name="Транспорт", color="#0000FF")
            await category.create(db, obj_in=category_in)
            await db.commit()

            # Получаем категорию по имени
            category_db = await category.get_by_name(db, name="Транспорт")
            assert category_db is not None
            assert category_db.name == "Транспорт"


@pytest.mark.asyncio
class TestCRUDUser:
    """Тесты CRUD операций для пользователей."""

    @pytest.fixture(autouse=True)
    async def setup_db(self):
        """Настройка тестовой БД."""
        self.engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

        # Создаем таблицы
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Создаем фабрику сессий
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

        yield

        # Очищаем таблицы
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await self.engine.dispose()

    async def test_create_user(self):
        """Тест создания пользователя."""
        async with self.AsyncSessionLocal() as db:
            user_in = UserCreate(email="test@example.com", username="test_user")
            user_obj = await user.create(db, obj_in=user_in)

            assert user_obj.id is not None
            assert user_obj.email == "test@example.com"
            assert user_obj.username == "test_user"

            await db.commit()

    async def test_get_by_email_user(self):
        """Тест получения пользователя по email."""
        async with self.AsyncSessionLocal() as db:
            # Создаем пользователя
            user_in = UserCreate(email="user@example.com", username="user123")
            await user.create(db, obj_in=user_in)
            await db.commit()

            # Получаем пользователя по email
            user_db = await user.get_by_email(db, email="user@example.com")
            assert user_db is not None
            assert user_db.email == "user@example.com"
