# Authentication Flow Documentation

**Feature**: 001-cleanup-functional-project
**Date**: 2026-02-09

## Overview

This document describes the authentication flow for the multi-user todo application, following the constitution requirement that Better Auth runs on the frontend and the backend performs stateless JWT verification.

## Architecture

```
┌─────────────┐                    ┌─────────────┐
│   Browser   │                    │   Backend   │
│  (Next.js)  │                    │  (FastAPI)  │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │  1. User submits credentials    │
       │  (email + password)              │
       ├─────────────────────────────────►│
       │                                  │
       │  2. Better Auth verifies &      │
       │     generates JWT token         │
       │◄─────────────────────────────────┤
       │                                  │
       │  3. Token stored in httpOnly    │
       │     cookie                       │
       │                                  │
       │  4. API request with JWT        │
       │     in Authorization header     │
       ├─────────────────────────────────►│
       │                                  │
       │  5. Backend verifies JWT        │
       │     using shared secret         │
       │                                  │
       │  6. Response with data          │
       │◄─────────────────────────────────┤
       │                                  │
```

## Components

### Frontend (Next.js + Better Auth)

**Responsibilities**:
- Handle user registration (signup)
- Handle user login (signin)
- Generate JWT tokens upon successful authentication
- Store tokens securely in httpOnly cookies
- Attach tokens to API requests
- Handle token refresh
- Manage user session state

**Technology**: Better Auth v1.x running in Next.js 16+ App Router

### Backend (FastAPI)

**Responsibilities**:
- Verify JWT tokens on protected endpoints
- Extract user context from valid tokens
- Return 401 Unauthorized for invalid/expired tokens
- NO user registration/login logic (handled by frontend)
- NO session storage (stateless)

**Technology**: FastAPI with python-jose for JWT verification

## Authentication Flows

### 1. User Registration Flow

```
User → Frontend (Better Auth) → Database (Neon)
```

**Steps**:
1. User fills registration form (email + password)
2. Frontend validates input (email format, password strength)
3. Better Auth hashes password with bcrypt
4. Better Auth creates user record in database
5. Better Auth generates JWT token
6. Frontend stores token in httpOnly cookie
7. User is redirected to dashboard

**Frontend Code** (conceptual):
```typescript
// app/auth/signup/page.tsx
import { signUp } from "@/lib/auth-client";

async function handleSignup(email: string, password: string) {
  const { data, error } = await signUp.email({
    email,
    password,
  });

  if (error) {
    // Handle error (show message to user)
    return;
  }

  // Redirect to dashboard
  router.push("/dashboard");
}
```

**No Backend Involvement**: Registration is entirely handled by Better Auth on frontend.

### 2. User Login Flow

```
User → Frontend (Better Auth) → Database (Neon) → Frontend stores token
```

**Steps**:
1. User fills login form (email + password)
2. Frontend sends credentials to Better Auth
3. Better Auth queries database for user by email
4. Better Auth verifies password hash
5. If valid, Better Auth generates JWT token
6. Frontend stores token in httpOnly cookie
7. User is redirected to dashboard

**Frontend Code** (conceptual):
```typescript
// app/auth/signin/page.tsx
import { signIn } from "@/lib/auth-client";

async function handleSignin(email: string, password: string) {
  const { data, error } = await signIn.email({
    email,
    password,
  });

  if (error) {
    // Handle error (invalid credentials)
    return;
  }

  // Redirect to dashboard
  router.push("/dashboard");
}
```

**No Backend Involvement**: Login is entirely handled by Better Auth on frontend.

### 3. Authenticated API Request Flow

```
User → Frontend → Backend (JWT verification) → Backend (process request) → Response
```

**Steps**:
1. User performs action (e.g., fetch tasks)
2. Frontend retrieves JWT token from cookie
3. Frontend makes API request with `Authorization: Bearer <token>` header
4. Backend middleware intercepts request
5. Backend verifies JWT signature using BETTER_AUTH_SECRET
6. Backend extracts user_id from JWT payload
7. Backend processes request with user context
8. Backend returns response

**Frontend Code** (conceptual):
```typescript
// lib/api-client.ts
async function getTasks(token: string) {
  const response = await fetch(`${API_URL}/api/tasks`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch tasks");
  }

  return response.json();
}
```

**Backend Code** (conceptual):
```python
# middleware/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# api/tasks.py
@router.get("/tasks")
async def get_tasks(auth: dict = Depends(verify_token)):
    user_id = auth["user_id"]
    # Fetch tasks for this user_id
```

### 4. Token Refresh Flow

```
Frontend → Better Auth → New token → Frontend updates cookie
```

**Steps**:
1. Frontend detects token is nearing expiration
2. Frontend calls Better Auth refresh endpoint
3. Better Auth validates refresh token
4. Better Auth generates new JWT token
5. Frontend updates httpOnly cookie

**Note**: Better Auth handles refresh automatically if configured.

### 5. Logout Flow

```
User → Frontend → Clear cookie → Redirect to login
```

**Steps**:
1. User clicks logout button
2. Frontend calls Better Auth signOut
3. Frontend clears httpOnly cookie
4. Frontend redirects to login page

**No Backend Involvement**: Logout is entirely frontend operation.

## JWT Token Structure

### Token Payload

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",  // user_id
  "email": "user@example.com",
  "iat": 1707516000,  // issued at (Unix timestamp)
  "exp": 1707519600   // expiration (Unix timestamp)
}
```

### Header

```json
{
  "alg": "HS256",     // HMAC SHA-256
  "typ": "JWT"
}
```

### Signature

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  BETTER_AUTH_SECRET
)
```

## Security Considerations

### Shared Secret

**Requirement**: Frontend and backend MUST use the same `BETTER_AUTH_SECRET`

**Configuration**:
```bash
# Frontend .env
BETTER_AUTH_SECRET=<generate-random-secret-min-32-chars>

# Backend .env
BETTER_AUTH_SECRET=<same-secret-as-frontend>
```

**Generation**:
```bash
# Generate secure random secret
openssl rand -hex 32
```

### Token Storage

**Frontend**: Tokens stored in httpOnly cookies
- ✅ Prevents XSS attacks (JavaScript cannot access)
- ✅ Automatically sent with requests to same origin
- ✅ Better Auth handles this automatically

**Backend**: NO token storage
- ✅ Stateless (no session database)
- ✅ Tokens verified on every request
- ✅ No server-side session management

### Token Expiration

**Default**: Tokens expire after 1 hour (configurable)
**Refresh**: Refresh tokens valid for 7 days (configurable)

### CORS Configuration

**Requirement**: Backend must accept requests from frontend origin

```python
# backend/src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### HTTPS in Production

**Requirement**: All communication must use HTTPS in production
- Prevents token interception
- Required for secure cookies
- Better Auth enforces this automatically in production mode

## Error Handling

### Frontend Errors

| Error | Cause | Handling |
|-------|-------|----------|
| Invalid credentials | Wrong email/password | Show error message to user |
| Network error | Backend unavailable | Show "Service unavailable" message |
| Token expired | User session expired | Redirect to login page |

### Backend Errors

| Status Code | Scenario | Response |
|-------------|----------|----------|
| 401 | Missing token | `{"detail": "Authentication required"}` |
| 401 | Invalid token | `{"detail": "Could not validate credentials"}` |
| 401 | Expired token | `{"detail": "Token has expired"}` |
| 403 | Valid token but insufficient permissions | `{"detail": "Not authorized"}` |

## Testing Authentication

### Manual Testing Checklist

1. **Registration**:
   - [ ] User can register with valid email and password
   - [ ] Registration fails with invalid email format
   - [ ] Registration fails with weak password
   - [ ] Duplicate email registration fails

2. **Login**:
   - [ ] User can login with correct credentials
   - [ ] Login fails with wrong password
   - [ ] Login fails with non-existent email

3. **Protected Routes**:
   - [ ] Unauthenticated requests return 401
   - [ ] Authenticated requests succeed
   - [ ] Users can only access their own data

4. **Token Expiration**:
   - [ ] Expired tokens are rejected
   - [ ] Token refresh works correctly

5. **Logout**:
   - [ ] User can logout successfully
   - [ ] Logged out users cannot access protected routes

### Testing with curl

```bash
# 1. Login is handled by frontend, not backend
# You would typically get a token from the browser dev tools

# 2. Test protected endpoint with token
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json"

# 3. Test without token (should return 401)
curl -X GET http://localhost:8000/api/tasks \
  -H "Content-Type: application/json"
```

## Environment Variables

### Frontend (.env)

```bash
# Better Auth configuration
BETTER_AUTH_SECRET=<your-secret-here>
DATABASE_URL=<neon-connection-string>

# API configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```bash
# JWT verification
BETTER_AUTH_SECRET=<same-secret-as-frontend>

# Database
DATABASE_URL=<neon-connection-string>

# CORS
FRONTEND_URL=http://localhost:3000
```

## Constitution Compliance Checklist

- [x] Better Auth runs only on frontend ✅
- [x] Backend is stateless (no session storage) ✅
- [x] JWT is the only authentication mechanism ✅
- [x] Shared secret via BETTER_AUTH_SECRET ✅
- [x] Authorization header for authenticated requests ✅
- [x] Encryption in transit (HTTPS in production) ✅
- [x] Stateless session management ✅

## Future Enhancements (Out of Scope)

- OAuth providers (Google, GitHub)
- Two-factor authentication (2FA)
- Password reset flow
- Email verification
- Rate limiting on auth endpoints
- Refresh token rotation
