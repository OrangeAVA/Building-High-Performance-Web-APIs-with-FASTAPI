from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select

# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/todo_db"  # Use asyncpg for PostgreSQL
DATABASE_URL = "mysql+aiomysql://user:password@localhost:3306/todo_db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# SessionLocal for async database session
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, future=True
)

Base = declarative_base()

# Dependency to get async DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
