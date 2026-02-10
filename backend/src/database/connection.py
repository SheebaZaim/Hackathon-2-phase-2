"""Database connection for Neon PostgreSQL with SQLModel"""
from sqlmodel import SQLModel, create_engine, Session, text
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Neon requires sslmode=require
if DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL = f"{DATABASE_URL}?sslmode=require"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10
)


def init_db():
    """Initialize database and create all tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


# For testing database connection
def test_connection():
    """Test database connection"""
    try:
        with Session(engine) as session:
            result = session.exec(text("SELECT 1"))
            result.one()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def get_engine():
    """Get database engine for testing"""
    return engine
