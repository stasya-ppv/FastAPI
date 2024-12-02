from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from sqlmodel import SQLModel
from models import MediaFile  # Импортируйте модели из вашего проекта
from alembic import context

# Этот объект для конфигурации Alembic
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Целевая метаинформация для моделей
target_metadata = SQLModel.metadata

def run_migrations_offline():
    """Миграции в оффлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Миграции в онлайн-режиме."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        connect_args={"client_encoding": "UTF8"}
    )

    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
