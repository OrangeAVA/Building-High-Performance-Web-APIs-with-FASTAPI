import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

# Add current working directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import your database Base
from database import Base

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Define metadata for autogenerate
target_metadata = Base.metadata

# Use your DB URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"

def run_migrations_offline():
    context.configure(
        url=SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
