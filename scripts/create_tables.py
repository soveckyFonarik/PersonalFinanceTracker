#!/usr/bin/env python3
"""
Создание таблиц в PostgreSQL через SQLAlchemy.
"""
import asyncio
import sys
from pathlib import Path
from typing import List, Tuple

# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import engine
from app.models import Base


async def create_tables():
    """Создает все таблицы в базе данных"""
    print("🗄️  Создание таблиц в PostgreSQL...")

    try:
        # Создаем таблицы через SQLAlchemy
        async with engine.begin() as conn:
            # Удаляем таблицы если они существуют (для разработки)
            print("⚠️  Удаление существующих таблиц...")
            await conn.run_sync(Base.metadata.drop_all)

            # Создаем таблицы
            print("📝 Создание новых таблиц...")
            await conn.run_sync(Base.metadata.create_all)

        print("✅ Таблицы успешно созданы!")

        # Показываем созданные таблицы - используем text() для запросов
        from sqlalchemy import text

        async with engine.connect() as conn:
            # Получаем список таблиц
            result = await conn.execute(
                text(
                    """
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """
                )
            )

            tables = [row[0] for row in result.fetchall()]
            print(f"\n📊 Созданные таблицы ({len(tables)}):")

            for table in tables:
                print(f"  • {table}")

                # Показываем колонки для каждой таблицы
                result = await conn.execute(
                    text(
                        """
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns
                        WHERE table_schema = 'public' 
                        AND table_name = :table_name
                        ORDER BY ordinal_position;
                    """
                    ),
                    {"table_name": table},
                )

                for col in result.fetchall():
                    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                    print(f"    - {col[0]}: {col[1]} {nullable}")

        return True

    except Exception as e:
        print(f"\n❌ Ошибка при создании таблиц: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Создание таблиц для Finance Tracker")
    print("=" * 60)
    print("ВНИМАНИЕ: Этот скрипт УДАЛИТ существующие данные!")
    print("=" * 60)

    # Подтверждение
    confirm = input("\nПродолжить? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Отменено пользователем")
        sys.exit(0)

    # Запускаем создание таблиц
    success = asyncio.run(create_tables())

    if success:
        print("\n🎉 Все таблицы успешно созданы!")
        print("\n📋 Следующие шаги:")
        print("1. Проверь таблицы: python scripts/check_tables.py")
        print("2. Добавь тестовые данные: python scripts/seed_data.py")
        print("3. Запусти API: python run.py")
    else:
        print("\n❌ Ошибка при создании таблиц")
        sys.exit(1)
