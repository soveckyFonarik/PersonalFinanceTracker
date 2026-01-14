"""
Тесты для API эндпоинтов категорий.
"""

import pytest
from uuid import uuid4
from httpx import AsyncClient


@pytest.mark.asyncio
class TestCategoriesAPI:
    """Тесты CRUD операций для категорий."""

    # async def test_create_category_success(self, client: AsyncClient):
    #     """Тест успешного создания категории."""
    #     category_data = {
    #         "name": "Тестовая категория",
    #         "description": "Описание тестовой категории",
    #         "color": "#FF5733",
    #     }

    #     response = await client.post("/api/v1/categories/", json=category_data)

    #     assert response.status_code == 201
    #     data = response.json()

    #     assert data["name"] == category_data["name"]
    #     assert data["description"] == category_data["description"]
    #     assert data["color"] == category_data["color"]
    #     assert "id" in data
    #     assert "created_at" in data
    #     assert "updated_at" in data

    #     # Сохраняем ID для последующих тестов
    #     TestCategoriesAPI.category_id = data["id"]

    # async def test_create_category_duplicate_name(self, client: AsyncClient):
    #     """Тест создания категории с дублирующимся именем."""
    #     category_data = {
    #         "name": "Дубликат категории",
    #         "description": "Описание",
    #         "color": "#FF5733",
    #     }

    #     # Первое создание
    #     response1 = await client.post("/api/v1/categories/", json=category_data)
    #     assert response1.status_code == 201

    #     # Второе создание с тем же именем
    #     response2 = await client.post("/api/v1/categories/", json=category_data)
    #     assert response2.status_code == 400
    #     data = response2.json()
    #     assert "уже существует" in data["detail"].lower()

    async def test_get_categories_list(self, client: AsyncClient):
        """Тест получения списка категорий."""
        response = await client.get("/api/v1/categories/")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

        # Проверяем пагинационные параметры
        response = await client.get(
            "/api/v1/categories/", params={"skip": 0, "limit": 5}
        )
        assert response.status_code == 200

    async def test_get_category_by_id_success(self, client: AsyncClient):
        """Тест успешного получения категории по ID."""
        if not hasattr(TestCategoriesAPI, "category_id"):
            pytest.skip("Нет созданной категории для теста")

        response = await client.get(
            f"/api/v1/categories/{TestCategoriesAPI.category_id}"
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == TestCategoriesAPI.category_id
        assert data["name"] == "Тестовая категория"
        assert data["description"] == "Описание тестовой категории"

    async def test_get_category_by_id_not_found(self, client: AsyncClient):
        """Тест получения несуществующей категории."""
        non_existent_id = str(uuid4())
        response = await client.get(f"/api/v1/categories/{non_existent_id}")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "не найдена" in data["detail"].lower()

    async def test_get_category_by_name_success(self, client: AsyncClient):
        """Тест получения категории по имени."""
        if not hasattr(TestCategoriesAPI, "category_id"):
            pytest.skip("Нет созданной категории для теста")

        response = await client.get("/api/v1/categories/name/Тестовая категория")

        # Эндпоинт может вернуть 200 с данными или null
        assert response.status_code == 200
        data = response.json()

        if data:  # Если категория найдена
            assert data["name"] == "Тестовая категория"

    # async def test_get_category_by_name_not_found(self, client: AsyncClient):
    #     """Тест получения категории по несуществующему имени."""
    #     response = await client.get("/api/v1/categories/name/НесуществующаяКатегория")

    #     assert response.status_code == 200
    #     data = response.json()

    #     # Эндпоинт возвращает null если категория не найдена
    #     assert data is None

    async def test_update_category_success(self, client: AsyncClient):
        """Тест успешного обновления категории."""
        if not hasattr(TestCategoriesAPI, "category_id"):
            pytest.skip("Нет созданной категории для теста")

        update_data = {
            "name": "Обновленное название",
            "description": "Обновленное описание",
            "color": "#00FF00",
        }

        response = await client.put(
            f"/api/v1/categories/{TestCategoriesAPI.category_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == TestCategoriesAPI.category_id
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["color"] == update_data["color"]

    async def test_update_category_duplicate_name(self, client: AsyncClient):
        """Тест обновления категории с именем другой категории."""
        # Создаем первую категорию
        cat1_data = {
            "name": "Категория 1",
            "description": "Описание",
            "color": "#FF0000",
        }
        response1 = await client.post("/api/v1/categories/", json=cat1_data)
        cat1_id = response1.json()["id"]

        # Создаем вторую категорию
        cat2_data = {
            "name": "Категория 2",
            "description": "Описание",
            "color": "#00FF00",
        }
        response2 = await client.post("/api/v1/categories/", json=cat2_data)
        cat2_id = response2.json()["id"]

        try:
            # Пытаемся переименовать вторую категорию в имя первой
            update_data = {"name": "Категория 1"}
            response = await client.put(
                f"/api/v1/categories/{cat2_id}", json=update_data
            )

            assert response.status_code == 400
            data = response.json()
            assert "уже существует" in data["detail"].lower()
        finally:
            # Очищаем тестовые данные
            await client.delete(f"/api/v1/categories/{cat1_id}")
            await client.delete(f"/api/v1/categories/{cat2_id}")

    async def test_delete_category_success(self, client: AsyncClient):
        """Тест успешного удаления категории."""
        if not hasattr(TestCategoriesAPI, "category_id"):
            pytest.skip("Нет созданной категории для теста")

        response = await client.delete(
            f"/api/v1/categories/{TestCategoriesAPI.category_id}"
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == TestCategoriesAPI.category_id

        # Проверяем что категория действительно удалена
        response = await client.get(
            f"/api/v1/categories/{TestCategoriesAPI.category_id}"
        )
        assert response.status_code == 404

    async def test_delete_category_not_found(self, client: AsyncClient):
        """Тест удаления несуществующей категории."""
        non_existent_id = str(uuid4())
        response = await client.delete(f"/api/v1/categories/{non_existent_id}")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "не найдена" in data["detail"].lower()
