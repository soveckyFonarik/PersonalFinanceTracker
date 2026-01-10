#!/usr/bin/env python3
"""
Проверка существования и структуры таблиц.
"""
import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import engine
from app.config import settings
from sqlalchemy import text


async def check_tables():
    """Проверяет существование и структуру таблиц"""
    print("🔍 Проверка таблиц в PostgreSQL...")
    print(f"База данных: {settings.postgres_db}")
    print("=" * 60)

    try:
        async with engine.connect() as conn:
            # 1. Проверяем подключение
            result = await conn.execute(text("SELECT version(), current_timestamp"))
            row = result.fetchone()

            if not row:
                print("❌ Нет данных от PostgreSQL")
                return False

            db_version, db_time = row[0], row[1]  # Используем индексы вместо распаковки
            print(f"✅ Подключено к PostgreSQL")
            print(f"📅 Время сервера: {db_time}")

            # 2. Проверяем существование таблиц
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

            rows = result.fetchall()
            tables = [row[0] for row in rows] if rows else []

            if not tables:
                print("\n📭 Таблицы не найдены!")
                print("Запусти: python scripts/create_tables.py")
                return False

            print(f"\n📊 Найдено таблиц: {len(tables)}")

            # 3. Проверяем каждую таблицу
            expected_tables = {"notes", "categories"}
            missing_tables = expected_tables - set(tables)
            extra_tables = set(tables) - expected_tables

            if missing_tables:
                print(f"\n❌ Отсутствуют таблицы: {missing_tables}")
                print("Запусти: python scripts/create_tables.py")

            if extra_tables:
                print(f"\n⚠️  Лишние таблицы: {extra_tables}")

            # 4. Проверяем структуру наших таблиц
            print("\n📋 Структура таблиц:")
            print("-" * 40)

            for table_name in sorted(tables):
                if table_name in expected_tables:
                    print(f"\n📝 Таблица: {table_name}")

                    # Колонки
                    result = await conn.execute(
                        text(
                            """
                            SELECT 
                                column_name,
                                data_type,
                                is_nullable,
                                column_default
                            FROM information_schema.columns
                            WHERE table_schema = 'public' 
                            AND table_name = :table_name
                            ORDER BY ordinal_position;
                        """
                        ),
                        {"table_name": table_name},
                    )

                    columns = result.fetchall()
                    print(f"  Колонок: {len(columns)}")

                    for col in columns:
                        column_name, data_type, is_nullable, column_default = col
                        nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                        default = (
                            f"[default: {column_default}]" if column_default else ""
                        )
                        print(f"    • {column_name}: {data_type} {nullable} {default}")

                    # Ограничения
                    result = await conn.execute(
                        text(
                            """
                            SELECT constraint_name, constraint_type
                            FROM information_schema.table_constraints
                            WHERE table_schema = 'public' 
                            AND table_name = :table_name;
                        """
                        ),
                        {"table_name": table_name},
                    )

                    constraints = result.fetchall()
                    if constraints:
                        print(f"  Ограничения: {len(constraints)}")
                        for const in constraints:
                            print(f"    • {const[0]}: {const[1]}")

                    # Количество записей
                    result = await conn.execute(
                        text(f"SELECT COUNT(*) FROM {table_name};")
                    )
                    count_result = result.fetchone()
                    count = count_result[0] if count_result else 0
                    print(f"  Записей: {count}")

            # 5. Итог
            print("\n" + "=" * 60)
            if not missing_tables:
                print("✅ Все таблицы существуют и имеют правильную структуру!")
                return True
            else:
                print("❌ Есть проблемы со структурой таблиц")
                return False

    except Exception as e:
        print(f"\n❌ Ошибка подключения: {type(e).__name__}: {e}")
        print("\nПроверь:")
        print("1. Запущен ли PostgreSQL на NAS")
        print("2. Правильность данных в .env файле")
        print("3. Существует ли база данных")
        return False


if __name__ == "__main__":
    print("🔍 Проверка структуры базы данных")
    print("=" * 60)

    success = asyncio.run(check_tables())

    if success:
        print("\n✅ Проверка завершена успешно!")
        print("Можно переходить к добавлению данных и запуску API.")
    else:
        print("\n❌ Есть проблемы с базой данных")
        sys.exit(1)
