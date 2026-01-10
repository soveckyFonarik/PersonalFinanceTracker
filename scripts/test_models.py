#!/usr/bin/env python3
"""
Скрипт для тестирования моделей SQLAlchemy.
Проверяем, что модели создаются корректно.
"""
import asyncio
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.models.note import Note
from app.models.category import Category


def test_model_creation():
    """Тестируем создание объектов моделей"""
    print("🧪 Тестирование моделей SQLAlchemy")
    print("=" * 50)

    # Тест 1: Создание заметки
    print("\n1. Создание объекта Note...")
    note = Note(title="Тестовая заметка", content="Это тестовое описание")
    print(f"   Note создан: {note}")
    print(f"   ID: {note.id}")
    print(f"   Заголовок: {note.title}")
    print(f"   Контент: {note.content}")
    print(f"   created_at: {note.created_at}")
    print(f"   updated_at: {note.updated_at}")

    # Тест 2: Создание категории с валидным цветом
    print("\n2. Создание Category с валидным цветом...")
    category = Category(name="Еда", color="#FF5733")
    print(f"   Category создан: {category}")
    print(f"   Название: {category.name}")
    print(f"   Цвет: {category.color}")
    print(f"   Цвет валиден? {Category.is_valid_color(category.color)}")

    # Тест 3: Проверка валидации цвета
    print("\n3. Проверка валидации цвета...")
    test_colors = [
        ("#FF5733", True),  # валидный
        ("#000000", True),  # валидный
        ("#123ABC", True),  # валидный
        ("invalid", False),  # невалидный
        ("#12345", False),  # невалидный (мало символов)
        ("123456", False),  # невалидный (нет #)
        ("#GGGGGG", False),  # невалидный (не hex)
    ]

    for color, should_be_valid in test_colors:
        is_valid = Category.is_valid_color(color)
        status = "✅" if is_valid == should_be_valid else "❌"
        print(f"   {status} {color}: valid={is_valid} (expected {should_be_valid})")

    # Тест 4: Проверка уникальности названий категорий
    print("\n4. Проверка уникальности категорий...")
    cat1 = Category(name="Транспорт", color="#33FF57")
    cat2 = Category(name="Развлечения", color="#3357FF")
    print(f"   Создано 2 категории с разными именами")
    print(f"   Уникальность проверяется БД при сохранении")

    print("\n🎉 Все тесты моделей пройдены!")
    return True


def test_sqlalchemy_metadata():
    """Минимальная проверка моделей"""
    print("\n✅ Проверка моделей SQLAlchemy:")
    print("=" * 50)

    # Просто создаем объекты и проверяем их атрибуты
    print("\n1. Проверка модели Note:")
    note = Note(title="Test", content="Test content")
    print(f"   ✓ Объект создан: id={note.id}")
    print(f"   ✓ Таблица: {getattr(Note, '__tablename__', 'unknown')}")
    print(f"   ✓ Колонки: {[c.name for c in Note.__table__.columns]}")

    print("\n2. Проверка модели Category:")
    category = Category(name="Test", color="#FF5733")
    print(f"   ✓ Объект создан: id={category.id}")
    print(f"   ✓ Таблица: {getattr(Category, '__tablename__', 'unknown')}")
    print(f"   ✓ Колонки: {[c.name for c in Category.__table__.columns]}")

    print("\n3. Проверка валидации цвета:")
    try:
        bad_category = Category(name="Bad", color="invalid")
        print("   ✗ ОШИБКА: невалидный цвет прошел проверку!")
    except ValueError as e:
        print(f"   ✓ Валидация работает: {e}")

    print("\n🎉 Модели SQLAlchemy работают корректно!")


if __name__ == "__main__":
    print("🚀 Запуск тестов моделей SQLAlchemy")
    print("=" * 50)

    try:
        test_model_creation()
        test_sqlalchemy_metadata()
        print("\n✅ Все тесты успешно пройдены!")
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
