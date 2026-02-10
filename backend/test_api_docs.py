"""Test API documentation endpoints"""
import requests
import json

print("=" * 60)
print("Testing API Documentation")
print("=" * 60)

BASE_URL = "http://127.0.0.1:8000"

# Test 1: OpenAPI JSON schema
print("\nTest 1: OpenAPI JSON Schema")
try:
    response = requests.get(f"{BASE_URL}/openapi.json")
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] OpenAPI JSON accessible")
        print(f"     Title: {data['info']['title']}")
        print(f"     Version: {data['info']['version']}")
        print(f"     Description: {data['info']['description'][:50]}...")

        # List all endpoints
        print(f"\n     Endpoints found:")
        for path in sorted(data['paths'].keys()):
            for method in data['paths'][path].keys():
                print(f"       {method.upper():6} {path}")
    else:
        print(f"[ERROR] Failed to access OpenAPI JSON: {response.status_code}")
except Exception as e:
    print(f"[ERROR] OpenAPI JSON test failed: {e}")

# Test 2: Swagger UI
print("\nTest 2: Swagger UI (/docs)")
try:
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        html = response.text
        if "swagger-ui" in html and "Todo App API" in html:
            print(f"[OK] Swagger UI accessible")
        else:
            print(f"[WARNING] Swagger UI page loaded but content may be incorrect")
    else:
        print(f"[ERROR] Failed to access Swagger UI: {response.status_code}")
except Exception as e:
    print(f"[ERROR] Swagger UI test failed: {e}")

# Test 3: ReDoc
print("\nTest 3: ReDoc (/redoc)")
try:
    response = requests.get(f"{BASE_URL}/redoc")
    if response.status_code == 200:
        html = response.text
        if "redoc" in html.lower() and "Todo App API" in html:
            print(f"[OK] ReDoc accessible")
        else:
            print(f"[WARNING] ReDoc page loaded but content may be incorrect")
    else:
        print(f"[ERROR] Failed to access ReDoc: {response.status_code}")
except Exception as e:
    print(f"[ERROR] ReDoc test failed: {e}")

# Test 4: Root endpoint
print("\nTest 4: Root Endpoint (/)")
try:
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Root endpoint accessible")
        print(f"     Message: {data.get('message')}")
        print(f"     Version: {data.get('version')}")
        print(f"     Docs: {data.get('docs')}")
        print(f"     Health: {data.get('health')}")
    else:
        print(f"[ERROR] Failed to access root endpoint: {response.status_code}")
except Exception as e:
    print(f"[ERROR] Root endpoint test failed: {e}")

print("\n" + "=" * 60)
print("API Documentation Tests Complete")
print("=" * 60)
