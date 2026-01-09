import pytest
from httpx import AsyncClient
from app.main import app
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_note():
    """Тест создания заметки"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/notes/", json={"title": "Test Note", "content": "Test content"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Note"
        assert "id" in data


@pytest.mark.asyncio
async def test_get_notes():
    """Тест получения списка заметок"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/notes/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_nonexistent_note():
    """Тест получения несуществующей заметки"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        non_existent_id = str(uuid4())
        print(f"Testing with UUID: {non_existent_id}")  # Для отладки
        response = await client.get(f"/notes/{non_existent_id}")

        print(f"Response status: {response.status_code}")  # Для отладки
        print(f"Response body: {response.text}")  # Для отладки

        assert response.status_code == 404
        assert response.json()["detail"] == "Note not found"
