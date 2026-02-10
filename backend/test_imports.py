"""Test backend imports and basic functionality"""
import sys
print(f"Python version: {sys.version}")

try:
    print("\n1. Testing FastAPI import...")
    from fastapi import FastAPI
    print("   [OK] FastAPI imported successfully")
except Exception as e:
    print(f"   [FAIL] FastAPI import failed: {e}")
    sys.exit(1)

try:
    print("\n2. Testing SQLModel import...")
    from sqlmodel import Session, create_engine
    print("   [OK] SQLModel imported successfully")
except Exception as e:
    print(f"   [FAIL] SQLModel import failed: {e}")
    sys.exit(1)

try:
    print("\n3. Testing python-jose import...")
    from jose import jwt
    print("   [OK] python-jose imported successfully")
except Exception as e:
    print(f"   [FAIL] python-jose import failed: {e}")
    sys.exit(1)

try:
    print("\n4. Testing database connection...")
    from src.database.connection import test_connection, get_engine
    engine = get_engine()
    print(f"   Database URL configured: {bool(engine)}")
    db_connected = test_connection()
    if db_connected:
        print("   [OK] Database connection successful")
    else:
        print("   [WARN] Database connection failed (check DATABASE_URL)")
except Exception as e:
    print(f"   [FAIL] Database test failed: {e}")

try:
    print("\n5. Testing main app import...")
    from src.main import app
    print(f"   [OK] Main app imported successfully")
    print(f"   App title: {app.title}")
    print(f"   Routes: {len(app.routes)}")
except Exception as e:
    print(f"   [FAIL] Main app import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("Import test complete!")
