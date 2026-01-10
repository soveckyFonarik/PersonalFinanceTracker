#!/usr/bin/env python3
"""
Добавление тестовых данных в базу.
"""
import asyncio
import sys
from pathlib import Path
from sqlalchemy import text

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Импортируем напрямую из database вместо database
from app.database import AsyncSessionLocal
from app.models.note import Note
from app.models.category import Category


async def seed_data():
    """Добавляет тестовые данные в базу"""
    print("🌱 Добавление тестовых данных...")

    try:
        async with AsyncSessionLocal() as session:
            # 1. Очищаем существующие данные (опционально)
            print("🧹 Очистка старых данных...")
            await session.execute(
                text("TRUNCATE TABLE notes, categories RESTART IDENTITY CASCADE;")
            )

            # 2. Создаем категории
            print("🗂️  Создание категорий...")
            categories_data = [
                {"name": "Еда", "color": "#FF5733"},
                {"name": "Транспорт", "color": "#33FF57"},
                {"name": "Развлечения", "color": "#3357FF"},
                {"name": "Коммунальные услуги", "color": "#F5FF33"},
                {"name": "Здоровье", "color": "#FF33F5"},
                {"name": "Образование", "color": "#33FFF5"},
                {"name": "Одежда", "color": "#F533FF"},
                {"name": "Подарки", "color": "#FF8C33"},
            ]

            categories = []
            for cat_data in categories_data:
                category = Category(**cat_data)
                session.add(category)
                categories.append(category)

            await session.flush()
            print(f"✅ Создано {len(categories)} категорий")

            # 3. Создаем заметки
            print("\n📝 Создание заметок...")
            notes_data = [
                {"title": "Продукты на неделю", "content": "Молоко, хлеб, яйца, овощи"},
                {"title": "Бензин", "content": "Заправить машину на неделю"},
                {"title": "Кино", "content": "Билеты на новый фильм Marvel"},
                {"title": "Электричество", "content": "Оплата за ноябрь"},
                {"title": "Визит к врачу", "content": "Ежегодный чек-ап"},
                {
                    "title": "Книги по Python",
                    "content": "Купить новые книги для обучения",
                },
                {"title": "Зимняя куртка", "content": "Нужна новая теплая куртка"},
                {
                    "title": "Подарок на день рождения",
                    "content": "Маме на день рождения",
                },
                {"title": "Обед в ресторане", "content": "Встреча с друзьями"},
                {"title": "Такси в аэропорт", "content": "Поездка в аэропорт в 6 утра"},
            ]

            notes = []
            for note_data in notes_data:
                note = Note(**note_data)
                session.add(note)
                notes.append(note)

            await session.commit()
            print(f"✅ Создано {len(notes)} заметок")

            # 4. Показываем результат
            print("\n📊 Тестовые данные добавлены:")
            print("\nКатегории:")
            for cat in categories:
                print(f"  • {cat.name} ({cat.color})")

            print("\nЗаметки:")
            for note in notes:
                preview = (
                    note.content[:30] + "..."
                    if len(note.content) > 30
                    else note.content
                )
                print(f"  • {note.title}: {preview}")

            print(
                f"\n🎉 Всего добавлено: {len(categories)} категорий и {len(notes)} заметок"
            )

            return True

    except Exception as e:
        print(f"\n❌ Ошибка при добавлении данных: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Добавление тестовых данных")
    print("=" * 60)
    print("ВНИМАНИЕ: Этот скрипт удалит существующие данные!")
    print("=" * 60)

    confirm = input("\nПродолжить? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Отменено пользователем")
        sys.exit(0)

    success = asyncio.run(seed_data())

    if success:
        print("\n✅ Тестовые данные успешно добавлены!")
        print("\n📋 Проверь данные:")
        print("python scripts/check_tables.py")
    else:
        print("\n❌ Ошибка при добавлении данных")
        sys.exit(1)
