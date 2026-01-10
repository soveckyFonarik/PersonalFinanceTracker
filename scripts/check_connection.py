import asyncio
import asyncpg
from app.config import settings


async def test_connection():
    """check connection"""
    print("🔌 Тестируем подключение к PostgreSQL...")
    print(f"Хост: {settings.postgres_host}:{settings.postgres_port}")
    print(f"База: {settings.postgres_db}")
    print(f"Пользователь: {settings.postgres_user}")
    print(f"Пароль: {settings.postgres_password}")

    try:
        conn = await asyncpg.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
        )

        version = await conn.fetchval("SELECT version();")
        print(f"✅ Успешно! Версия PostgreSQL: {version}")
        # Проверяем существующие таблицы
        tables = await conn.fetch(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """
        )

        if tables:
            print(f"\n📊 Найдено таблиц: {len(tables)}")
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("\n📭 Таблиц пока нет")

        await conn.close()

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        print("\nПроверь:")
        print("1. Правильность данных в .env")
        print("2. Запущен ли PostgreSQL на NAS")
        print("3. Доступен ли порт 5432")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)
