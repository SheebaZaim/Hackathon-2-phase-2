from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import Pool
import os
from typing import Generator
from urllib.parse import urlparse

# Get database URL from environment - default to SQLite for local testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

def create_db_engine():
    """Create database engine with appropriate settings for different databases"""
    if DATABASE_URL.startswith("sqlite"):
        # SQLite configuration
        return create_engine(
            DATABASE_URL,
            echo=True,  # Set to False in production
            connect_args={"check_same_thread": False}  # Required for SQLite
        )
    else:
        # PostgreSQL configuration (including Neon)
        # Parse the database URL to add SSL mode for Neon
        parsed_url = urlparse(DATABASE_URL)
        if 'neon' in parsed_url.hostname or 'neon' in DATABASE_URL.lower():
            # Add SSL mode require for Neon
            return create_engine(
                DATABASE_URL,
                echo=True,  # Set to False in production
                connect_args={"sslmode": "require"}  # SSL mode for Neon
            )
        else:
            # Standard PostgreSQL configuration
            return create_engine(
                DATABASE_URL,
                echo=True,  # Set to False in production
                connect_args={"sslmode": "require"}  # Require SSL for security
            )

# Create engine
engine = create_db_engine()

def get_session() -> Generator[Session, None, None]:
    """Get a database session"""
    with Session(engine) as session:
        yield session

# Optional: Add connection pool event listeners for debugging
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragma for foreign key support (only needed for SQLite)"""
    if DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()