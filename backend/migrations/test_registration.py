"""
Test script to verify registration works after migration
Usage: python test_registration.py
"""
import requests
import sys
from datetime import datetime

BACKEND_URL = "http://localhost:8000"
TEST_EMAIL = f"test_{datetime.now().timestamp()}@example.com"
TEST_PASSWORD = "password123"


def test_registration():
    """Test user registration endpoint"""

    print("=" * 60)
    print("Testing Registration Endpoint")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Email: {TEST_EMAIL}")
    print()

    # Check health first
    print("1. Checking backend health...")
    try:
        health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   ✅ Backend is {health_data['status']}")
            print(f"   ✅ Database is {health_data['database']}")
        else:
            print(f"   ❌ Health check failed: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        print("   Make sure backend is running: uvicorn src.main:app --reload")
        return False

    print()

    # Test registration
    print("2. Testing registration...")
    try:
        register_response = requests.post(
            f"{BACKEND_URL}/auth/register",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            },
            timeout=10
        )

        if register_response.status_code == 200:
            data = register_response.json()
            print(f"   ✅ Registration successful!")
            print(f"   ✅ Received access token: {data['access_token'][:50]}...")
            print(f"   ✅ Token type: {data['token_type']}")
            return True
        else:
            print(f"   ❌ Registration failed with status {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return False

    except Exception as e:
        print(f"   ❌ Registration request failed: {e}")
        return False


if __name__ == "__main__":
    print()
    success = test_registration()
    print()
    print("=" * 60)

    if success:
        print("✅ ALL TESTS PASSED!")
        print()
        print("Next steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Click 'Get Started' to register")
        print("3. Create some tasks in the dashboard")
        print()
        sys.exit(0)
    else:
        print("❌ TESTS FAILED!")
        print()
        print("If you see 'null value in column first_name':")
        print("  → Run the migration: python run_migration.py 001_fix_users_table_nullable_fields.sql")
        print()
        print("If you see 'Cannot connect to backend':")
        print("  → Start backend: uvicorn src.main:app --reload")
        print()
        sys.exit(1)
