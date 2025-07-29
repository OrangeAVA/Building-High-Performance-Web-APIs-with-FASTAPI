from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

# Import your models so Alembic knows them
from database import Base
from models import ToDoItem  # 👈 Make sure to import all models here

# Load Alembic config
config = context.config

# Setup logging
fileConfig(config.config_file_name)

# Provide metadata for Alembic to generate migrations
target_metadata = Base.metadata

# Database URL (sync version)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/todo_db"

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
