import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from core.config import settings
from core.database.base import Base


from models.admin.librarian import librarian
from models.books.book import Book
from models.library.borrowed import BorrowedBook
from models.users.reader import Reader


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    
    connectable = create_async_engine(settings.DATABASE_URL)
    
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_online() -> None:
    
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()