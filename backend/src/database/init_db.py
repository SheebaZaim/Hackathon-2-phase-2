"""Database initialization script for Todo App"""
from .connection import init_db, test_connection


def main():
    """Initialize database tables"""
    print("Testing database connection...")
    if not test_connection():
        print("❌ Database connection failed. Check DATABASE_URL in .env")
        return False

    print("✅ Database connection successful")

    print("Creating database tables...")
    try:
        init_db()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False


if __name__ == "__main__":
    main()
