# app/db/seed.py
"""
Модуль для заполнения базы данных начальными данными.
"""

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.note import Note
from app.models.category import Category
from app.core.config import settings


async def seed_categories(session: AsyncSession) -> list[Category]:
    """Создание категорий"""
    categories_data = [
        {
            "name": "🍔 Еда",
            "description": "Продукты, кафе, рестораны",
            "color": "#FF5733",
        },
        {
            "name": "🚗 Транспорт",
            "description": "Бензин, такси, общественный транспорт",
            "color": "#33FF57",
        },
        {
            "name": "🏠 Жилье",
            "description": "Аренда, ипотека, коммунальные услуги",
            "color": "#3357FF",
        },
        {
            "name": "💼 Работа",
            "description": "Зарплата, бизнес, инвестиции",
            "color": "#F5FF33",
        },
        {
            "name": "🎯 Развлечения",
            "description": "Кино, концерты, хобби",
            "color": "#FF33F5",
        },
        {
            "name": "🏥 Здоровье",
            "description": "Лекарства, врачи, спорт",
            "color": "#33FFF5",
        },
        {
            "name": "📚 Образование",
            "description": "Курсы, книги, обучение",
            "color": "#F533FF",
        },
        {
            "name": "👕 Одежда",
            "description": "Одежда, обувь, аксессуары",
            "color": "#FF8C33",
        },
        {
            "name": "🎁 Подарки",
            "description": "Подарки, благотворительность",
            "color": "#33FF8C",
        },
        {
            "name": "✈️ Путешествия",
            "description": "Отдых, отели, билеты",
            "color": "#8C33FF",
        },
    ]

    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        session.add(category)
        categories.append(category)

    await session.flush()
    return categories


async def seed_notes(session: AsyncSession) -> list[Note]:
    """Создание заметок"""
    notes_data = [
        {
            "title": "Продукты на неделю",
            "content": "Молоко, хлеб, яйца, овощи, фрукты, мясо, рыба",
        },
        {"title": "Заправка автомобиля", "content": "Бензин на неделю, масло, мойка"},
        {
            "title": "Оплата коммунальных услуг",
            "content": "Электричество, вода, газ, интернет за ноябрь",
        },
        {
            "title": "Зарплата за ноябрь",
            "content": "Основная зарплата + премия за проект",
        },
        {"title": "Билеты в кино", "content": "На фильм 'Мстители' на субботу вечером"},
        {"title": "Визит к стоматологу", "content": "Плановый осмотр, чистка зубов"},
        {
            "title": "Книги по программированию",
            "content": "'Чистая архитектура', 'Python Cookbook'",
        },
        {"title": "Зимняя одежда", "content": "Куртка, шапка, перчатки на зиму"},
        {
            "title": "Подарок маме",
            "content": "Цветы, конфеты, открытка на день рождения",
        },
        {
            "title": "Билеты на Бали",
            "content": "Авиабилеты, отель, страховка на февраль",
        },
    ]

    notes = []
    for note_data in notes_data:
        note = Note(**note_data)
        session.add(note)
        notes.append(note)

    await session.flush()
    return notes


async def seed_database(clear_existing: bool = False) -> dict:
    """
    Основная функция для заполнения базы данных.

    Args:
        clear_existing: Очистить существующие данные

    Returns:
        Словарь с результатами
    """
    print("🌱 Начало заполнения базы данных...")

    results = {
        "categories_created": 0,
        "notes_created": 0,
        "success": False,
        "error": None,
    }

    try:
        async with AsyncSessionLocal() as session:
            if clear_existing:
                print("🧹 Очистка существующих данных...")
                await session.execute(text("DELETE FROM notes;"))
                await session.execute(text("DELETE FROM categories;"))
                await session.commit()
                print("✅ Существующие данные очищены")

            # Создаем категории
            print("🗂️  Создание категорий...")
            categories = await seed_categories(session)
            results["categories_created"] = len(categories)
            print(f"✅ Создано {len(categories)} категорий")

            # Создаем заметки
            print("📝 Создание заметок...")
            notes = await seed_notes(session)
            results["notes_created"] = len(notes)
            print(f"✅ Создано {len(notes)} заметок")

            # Коммитим изменения
            await session.commit()
            results["success"] = True

            # Выводим краткую статистику
            print("\n📊 Статистика:")
            print(f"   • Категории: {len(categories)}")
            print(f"   • Заметки: {len(notes)}")
            print("✅ Данные успешно добавлены в базу")

            return results

    except Exception as e:
        results["error"] = str(e)
        print(f"❌ Ошибка при заполнении базы: {e}")
        import traceback

        traceback.print_exc()
        return results


async def check_if_database_empty() -> bool:
    """
    Проверяет, пустая ли база данных.

    Returns:
        True если база пустая, False если есть данные
    """
    try:
        async with AsyncSessionLocal() as session:
            # Проверяем категории
            categories_count = await session.execute(
                text("SELECT COUNT(*) FROM categories")
            )
            cat_count = categories_count.scalar()

            # Проверяем заметки
            notes_count = await session.execute(text("SELECT COUNT(*) FROM notes"))
            note_count = notes_count.scalar()

            return cat_count == 0 and note_count == 0

    except Exception as e:
        # Если таблиц нет, считаем базу пустой
        print(f"⚠️  При проверке базы: {e}")
        return True


async def seed_if_empty() -> bool:
    """
    Заполняет базу данных, только если она пустая.

    Returns:
        True если данные были добавлены, False если база уже заполнена
    """
    print("🔍 Проверка состояния базы данных...")

    is_empty = await check_if_database_empty()

    if is_empty:
        print("📭 База данных пустая, начинаем заполнение...")
        result = await seed_database(clear_existing=False)
        return result["success"]
    else:
        print("📊 База данных уже содержит данные, пропускаем заполнение")

        # Показываем статистику
        async with AsyncSessionLocal() as session:
            categories_count = await session.execute(
                text("SELECT COUNT(*) FROM categories")
            )
            notes_count = await session.execute(text("SELECT COUNT(*) FROM notes"))

            print(f"   • Категорий: {categories_count.scalar()}")
            print(f"   • Заметок: {notes_count.scalar()}")

        return False
