import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models.base import Base  # Импорт вашей базовой модели

# Загружаем конфигурацию Alembic
config = context.config

# Настраиваем логирование, если указано в конфигурации
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Получаем metadata из вашей ORM-модели
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме (без подключения к базе)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Функция для выполнения миграций в синхронном режиме через run_sync"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме (с подключением к базе)."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
