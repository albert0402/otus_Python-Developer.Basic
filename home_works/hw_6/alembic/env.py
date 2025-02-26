import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from config import db_url  # Import the database URL from the config
from models.base import Base  # Import the base model class

# Logging configuration
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set metadata for Alembic migrations
target_metadata = Base.metadata  


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in online mode using an asynchronous engine."""
    connectable = create_async_engine(db_url, poolclass=pool.NullPool, echo=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Helper function to run migrations with a given connection."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


# Determine whether to run migrations in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())