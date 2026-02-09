from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .base import Base
import os


# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Create async engine
engine = create_async_engine(DATABASE_URL)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session():
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """Initialize the database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)