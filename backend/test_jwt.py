"""Test JWT token verification"""
from src.services.auth import verify_jwt_token, extract_user_id
from jose import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("Testing JWT Verification")
print("=" * 60)

# Get secret from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    print("[ERROR] BETTER_AUTH_SECRET not found in environment")
    exit(1)

print(f"[OK] BETTER_AUTH_SECRET found: {SECRET_KEY[:10]}...")

# Create a test token
test_payload = {
    "sub": "test-user-id-12345",
    "email": "test@example.com",
    "exp": datetime.utcnow() + timedelta(hours=1)
}
test_token = jwt.encode(test_payload, SECRET_KEY, algorithm="HS256")

print(f"[OK] Test token created: {test_token[:50]}...")

# Test 1: Verify valid token
print("\nTest 1: Verify valid token")
try:
    payload = verify_jwt_token(test_token)
    print(f"[OK] Token verified successfully")
    print(f"     Payload: {payload}")
except Exception as e:
    print(f"[ERROR] Token verification failed: {e}")

# Test 2: Extract user ID
print("\nTest 2: Extract user ID")
try:
    user_id = extract_user_id(test_token)
    print(f"[OK] User ID extracted: {user_id}")
    if user_id == "test-user-id-12345":
        print("[OK] User ID matches expected value")
    else:
        print(f"[ERROR] User ID mismatch: expected 'test-user-id-12345', got '{user_id}'")
except Exception as e:
    print(f"[ERROR] User ID extraction failed: {e}")

# Test 3: Expired token
print("\nTest 3: Expired token rejection")
expired_payload = {
    "sub": "test-user-id-expired",
    "email": "expired@example.com",
    "exp": datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago
}
expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm="HS256")

try:
    payload = verify_jwt_token(expired_token)
    print(f"[ERROR] Expired token should have been rejected but was accepted")
except Exception as e:
    print(f"[OK] Expired token correctly rejected: {str(e)[:50]}...")

# Test 4: Invalid token
print("\nTest 4: Invalid token rejection")
try:
    payload = verify_jwt_token("invalid.token.here")
    print(f"[ERROR] Invalid token should have been rejected but was accepted")
except Exception as e:
    print(f"[OK] Invalid token correctly rejected: {str(e)[:50]}...")

print("\n" + "=" * 60)
print("JWT Verification Tests Complete")
print("=" * 60)
