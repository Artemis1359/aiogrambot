import asyncio
from logging.config import fileConfig

from sqlalchemy import pool, create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from aiogrambot.config import settings
from aiogrambot.database.db import Base
from aiogrambot.database import models



config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.get_db_url())

target_metadata = Base.metadata

connectable = create_engine(
    settings.get_db_sync_url(),
    poolclass=pool.NullPool,
)

# Async для upgrade
async_connectable = create_async_engine(
    settings.get_db_url(),
    poolclass=pool.NullPool,
)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection,
                      target_metadata=target_metadata,
                      compare_type=True,)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online_sync():
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

async def run_migrations_online_async():

    async with async_connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await async_connectable.dispose()

# def do_run_migrations(connection):
#     context.configure(connection=connection, target_metadata=target_metadata)
#     with context.begin_transaction():
#         context.run_migrations()

def run_migrations_online():
    import sys
    if "revision" in sys.argv or "stamp" in sys.argv:
        run_migrations_online_sync()
    else:
        asyncio.run(run_migrations_online_async())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
