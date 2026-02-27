# app/migration/env.py
import asyncio
from logging.config import fileConfig
import sys
from pathlib import Path
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from alembic import context

sys.path.insert(0, str(Path(__file__).parents[2]))

from app.users.models import User
from app.hobbies.models import Hobby
from app.languages.models import Language
from app.travel_goals.models import TravelGoal
from app.users.associative_tables.models import UserHobby, UserTravelGoal, UserLanguage

from app.posts.models import Post
from app.comments.models import Comment
from app.likes.models import Like

from app.database import Base
from app.configurator import get_db_url

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

async_url = get_db_url()
sync_url = async_url.replace("mysql+aiomysql://", "mysql+pymysql://")
config.set_main_option("sqlalchemy.url", sync_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,    
        compare_server_default=True, 
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (СИНХРОННЫЙ движок)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()