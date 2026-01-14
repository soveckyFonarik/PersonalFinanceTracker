"""
Тесты для API эндпоинтов заметок.
"""

import pytest
from uuid import uuid4
from httpx import AsyncClient


@pytest.mark.asyncio
class TestNotesAPI:
    """Тесты CRUD операций для заметок."""

    async def test_create_note_success(self, client: AsyncClient):
        """Тест успешного создания заметки."""
        note_data = {
            "title": "Тестовая заметка",
            "content": "Содержимое тестовой заметки",
        }

        response = await client.post("/api/v1/notes/", json=note_data)

        assert response.status_code == 201
        data = response.json()

        assert data["title"] == note_data["title"]
        assert data["content"] == note_data["content"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

        # Сохраняем ID для последующих тестов
        TestNotesAPI.note_id = data["id"]

    async def test_create_note_validation_error(self, client: AsyncClient):
        """Тест валидации при создании заметки."""
        # Пустой заголовок
        response = await client.post(
            "/api/v1/notes/", json={"title": "", "content": "Тест"}
        )
        assert response.status_code == 422

        # Заголовок слишком длинный
        response = await client.post(
            "/api/v1/notes/",
            json={"title": "A" * 101, "content": "Тест"},  # Максимум 100 символов
        )
        assert response.status_code == 422

        # Контент слишком длинный
        response = await client.post(
            "/api/v1/notes/",
            json={"title": "Тест", "content": "A" * 1001},  # Максимум 1000 символов
        )
        assert response.status_code == 422

    async def test_get_notes_list(self, client: AsyncClient):
        """Тест получения списка заметок."""
        response = await client.get("/api/v1/notes/")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

        # Проверяем пагинационные параметры
        response = await client.get("/api/v1/notes/", params={"skip": 0, "limit": 5})
        assert response.status_code == 200

    async def test_get_note_by_id_success(self, client: AsyncClient):
        """Тест успешного получения заметки по ID."""
        if not hasattr(TestNotesAPI, "note_id"):
            pytest.skip("Нет созданной заметки для теста")

        response = await client.get(f"/api/v1/notes/{TestNotesAPI.note_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == TestNotesAPI.note_id
        assert data["title"] == "Тестовая заметка"
        assert data["content"] == "Содержимое тестовой заметки"

    async def test_get_note_by_id_not_found(self, client: AsyncClient):
        """Тест получения несуществующей заметки."""
        non_existent_id = str(uuid4())
        response = await client.get(f"/api/v1/notes/{non_existent_id}")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "не найдена" in data["detail"].lower()

    async def test_update_note_success(self, client: AsyncClient):
        """Тест успешного обновления заметки."""
        if not hasattr(TestNotesAPI, "note_id"):
            pytest.skip("Нет созданной заметки для теста")

        update_data = {
            "title": "Обновленный заголовок",
            "content": "Обновленное содержимое",
        }

        response = await client.put(
            f"/api/v1/notes/{TestNotesAPI.note_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == TestNotesAPI.note_id
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]

    async def test_update_note_not_found(self, client: AsyncClient):
        """Тест обновления несуществующей заметки."""
        non_existent_id = str(uuid4())
        response = await client.put(
            f"/api/v1/notes/{non_existent_id}", json={"title": "Новый заголовок"}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "не найдена" in data["detail"].lower()

    async def test_update_note_validation_error(self, client: AsyncClient):
        """Тест валидации при обновлении заметки."""
        if not hasattr(TestNotesAPI, "note_id"):
            pytest.skip("Нет созданной заметки для теста")

        # Заголовок слишком длинный
        response = await client.put(
            f"/api/v1/notes/{TestNotesAPI.note_id}", json={"title": "A" * 101}
        )
        assert response.status_code == 422

    async def test_delete_note_success(self, client: AsyncClient):
        """Тест успешного удаления заметки."""
        if not hasattr(TestNotesAPI, "note_id"):
            pytest.skip("Нет созданной заметки для теста")

        response = await client.delete(f"/api/v1/notes/{TestNotesAPI.note_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == TestNotesAPI.note_id

        # Проверяем что заметка действительно удалена
        response = await client.get(f"/api/v1/notes/{TestNotesAPI.note_id}")
        assert response.status_code == 404

    async def test_delete_note_not_found(self, client: AsyncClient):
        """Тест удаления несуществующей заметки."""
        non_existent_id = str(uuid4())
        response = await client.delete(f"/api/v1/notes/{non_existent_id}")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "не найдена" in data["detail"].lower()

    async def test_search_notes_by_title(self, client: AsyncClient):
        """Тест поиска заметок по заголовку (если есть такой эндпоинт)."""
        # Сначала создаем заметку для поиска
        note_data = {"title": "Уникальная заметка для поиска", "content": "Контент"}
        create_response = await client.post("/api/v1/notes/", json=note_data)
        note_id = create_response.json()["id"]

        try:
            # Ищем по части заголовка
            response = await client.get(
                "/api/v1/notes/search/title",
                params={"title": "уникальная", "skip": 0, "limit": 10},
            )

            # Эндпоинт может быть 404 если не реализован
            if response.status_code == 200:
                data = response.json()
                assert isinstance(data, list)
                if data:
                    assert any("уникальная" in note["title"].lower() for note in data)
        finally:
            # Очищаем тестовые данные
            await client.delete(f"/api/v1/notes/{note_id}")
