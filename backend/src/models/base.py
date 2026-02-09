from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class Base(SQLModel):
    """Base class for all database models."""
    pass


# Create async database session maker
AsyncDatabaseSession = sessionmaker(class_=AsyncSession, expire_on_commit=False)


def create_db_and_tables(engine):
    """Create database tables."""
    SQLModel.metadata.create_all(engine)