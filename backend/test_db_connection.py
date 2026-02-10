"""Test database connection and table creation"""
from src.database.connection import test_connection, get_engine
from sqlmodel import text, Session

print("=" * 60)
print("Testing Database Connection")
print("=" * 60)

engine = get_engine()
print(f"Database URL: {str(engine.url).split('@')[1] if '@' in str(engine.url) else 'Not configured'}")
print(f"SSL mode: {'sslmode=require' in str(engine.url)}")

if test_connection():
    print("[OK] Database connection successful")

    # Test table creation
    from src.database.init_db import init_db
    try:
        init_db()
        print("[OK] Tables created/verified successfully")
    except Exception as e:
        print(f"[WARNING] Table initialization: {e}")

    # Verify tables exist
    with Session(engine) as session:
        result = session.exec(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.all()]
        print(f"[OK] Tables found in database: {tables}")

        # Check for our specific tables
        if 'users' in tables and 'tasks' in tables:
            print("[OK] Both 'users' and 'tasks' tables exist")
        else:
            print("[ERROR] Missing required tables")
else:
    print("[ERROR] Database connection failed")

print("=" * 60)
