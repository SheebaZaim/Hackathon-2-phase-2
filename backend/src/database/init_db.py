import asyncio
from .session import engine, AsyncSessionLocal
from ..models.base import Base
from sqlalchemy import text


async def init_db():
    """Initialize the database and create tables."""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def test_connection():
    """Test database connection."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(init_db())
    print("Database initialized successfully!")