# Technology Research: Project Cleanup and Functional Setup

**Feature**: 001-cleanup-functional-project
**Date**: 2026-02-09
**Status**: Complete

## Overview

This document captures research findings for implementing a clean, functional multi-user todo application following the constitution's fixed technology stack: Next.js 16+ (App Router), Python FastAPI, SQLModel, Neon Serverless PostgreSQL, and Better Auth + JWT.

## 1. Better Auth Integration with Next.js 16+

### Decision
Use Better Auth v1.x with Next.js 16 App Router, configured in the `src/lib/auth.ts` file with server-side authentication checks and client-side session management.

### Rationale
- Better Auth is designed specifically for Next.js with first-class App Router support
- Provides built-in JWT token generation and secure cookie storage
- Handles authentication flows (signup, signin, signout) with minimal configuration
- Supports database adapters including PostgreSQL via Prisma or raw SQL

### Configuration Pattern

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
  },
  secret: process.env.BETTER_AUTH_SECRET,
  trustedOrigins: [process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000"],
});

export type Session = typeof auth.$Infer.Session;
```

### Environment Variables
```
BETTER_AUTH_SECRET=<generate-random-secret>
DATABASE_URL=<neon-connection-string>
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Alternatives Considered
- **NextAuth.js**: More established but heavier, requires additional configuration
- **Clerk**: Third-party service, adds external dependency
- **Custom JWT implementation**: More control but significantly more code and security considerations

### Best Practices
- Store BETTER_AUTH_SECRET in environment variables, never commit
- Use httpOnly cookies for token storage (automatic with Better Auth)
- Implement CSRF protection (built into Better Auth)
- Validate sessions on protected routes using middleware

## 2. FastAPI JWT Verification

### Decision
Use `python-jose` for JWT verification in FastAPI middleware, with a dependency injection pattern for protected routes.

### Rationale
- `python-jose` is the recommended JWT library for FastAPI
- Supports RSA and HMAC signing algorithms
- Integrates seamlessly with FastAPI's dependency injection
- Provides clear error handling for expired/invalid tokens

### Implementation Pattern

```python
# backend/src/middleware/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt
from datetime import datetime
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

async def verify_token(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return {"user_id": user_id, "payload": payload}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# Usage in routes
@router.get("/tasks")
async def get_tasks(auth_data: dict = Depends(verify_token)):
    user_id = auth_data["user_id"]
    # ... fetch tasks for user_id
```

### Environment Variables
```
BETTER_AUTH_SECRET=<same-secret-as-frontend>
```

### Alternatives Considered
- **PyJWT**: Simpler but less feature-rich
- **Authlib**: More comprehensive but heavier
- **Custom implementation**: Not recommended due to security complexity

### Best Practices
- Share the same secret between frontend and backend
- Always validate token expiration
- Use dependency injection for route protection
- Return 401 for invalid/expired tokens
- Include user context in JWT payload (user_id, email)

## 3. Neon PostgreSQL Connection with SQLModel

### Decision
Use SQLModel with `psycopg2` adapter for synchronous database operations with Neon Serverless PostgreSQL.

### Rationale
- SQLModel provides Pydantic integration with FastAPI
- Neon supports standard PostgreSQL connection protocols
- Synchronous operations are simpler for CRUD operations
- Connection pooling handled by SQLModel/SQLAlchemy engine

### Connection Pattern

```python
# backend/src/database/connection.py
from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Neon requires sslmode=require
if DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL = f"{DATABASE_URL}?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### Neon Connection String Format
```
DATABASE_URL=postgresql://user:password@ep-xxx-yyy.region.aws.neon.tech/dbname?sslmode=require
```

### Alternatives Considered
- **Async SQLModel**: More complex, not needed for initial implementation
- **Prisma**: TypeScript-first, doesn't fit Python backend
- **Raw psycopg2**: More control but loses ORM benefits

### Best Practices
- Always use `sslmode=require` for Neon connections
- Enable `pool_pre_ping` to handle connection drops
- Use connection pooling (5-10 connections for small apps)
- Separate read/write operations if scaling needed
- Handle connection errors gracefully with retry logic

## 4. Next.js + FastAPI Communication

### Decision
Use native `fetch` API in Next.js with a centralized API client, configure CORS in FastAPI to allow frontend origin.

### Rationale
- Native `fetch` is built into Next.js 16, no extra dependencies
- Centralized client simplifies error handling and auth header injection
- CORS middleware in FastAPI is straightforward to configure

### API Client Pattern

```typescript
// frontend/src/lib/api-client.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiClient {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "API request failed");
    }

    return response.json();
  }

  async getTasks(token: string) {
    return this.request("/api/tasks", {
      headers: { Authorization: `Bearer ${token}` },
    });
  }
}

export const apiClient = new ApiClient();
```

### CORS Configuration (FastAPI)

```python
# backend/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        os.getenv("FRONTEND_URL", ""),  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Alternatives Considered
- **Axios**: Popular but adds dependency, fetch is sufficient
- **SWR/React Query**: Great for caching but adds complexity
- **tRPC**: Couples frontend/backend, violates separation requirement

### Best Practices
- Centralize API calls in a single client class
- Use environment variables for API URL
- Include error handling for network failures
- Add request/response interceptors for auth tokens
- Configure CORS to only allow specific origins in production

## 5. Responsive UI Best Practices

### Decision
Use TailwindCSS with mobile-first responsive design, leverage built-in utility classes for breakpoints.

### Rationale
- TailwindCSS is the most popular utility-first CSS framework
- Mobile-first approach ensures good mobile experience
- Built-in responsive breakpoints (sm, md, lg, xl, 2xl)
- No additional UI library needed for simple, clean designs

### Responsive Design Pattern

```tsx
// Example: Simple task card component
export function TaskCard({ task }) {
  return (
    <div className="
      w-full
      p-4 md:p-6
      bg-white dark:bg-gray-800
      rounded-lg
      shadow-sm hover:shadow-md
      transition-shadow
    ">
      <h3 className="text-lg md:text-xl font-semibold mb-2">
        {task.title}
      </h3>
      <p className="text-sm md:text-base text-gray-600 dark:text-gray-400">
        {task.description}
      </p>
    </div>
  );
}
```

### TailwindCSS Breakpoints
- `sm`: 640px (small tablets)
- `md`: 768px (tablets)
- `lg`: 1024px (laptops)
- `xl`: 1280px (desktops)
- `2xl`: 1536px (large desktops)

### Design Guidelines
- **Mobile-first**: Base styles for mobile, add breakpoints for larger screens
- **Typography**: Use responsive font sizes (text-sm → text-base → text-lg)
- **Spacing**: Adjust padding/margins at breakpoints (p-4 → md:p-6)
- **Layout**: Stack on mobile, grid on desktop (flex-col → md:flex-row)
- **Colors**: Use semantic color system (primary, secondary, accent)
- **Dark mode**: Support with `dark:` variants

### Alternatives Considered
- **Bootstrap**: Component-heavy, conflicts with custom design
- **Material-UI**: Too opinionated, adds significant bundle size
- **Chakra UI**: Good but adds abstraction layer
- **Plain CSS**: More control but slower development

### Best Practices
- Use Tailwind's `@apply` directive sparingly (prefer utility classes)
- Extract repeated patterns into components, not CSS classes
- Use `clsx` or `cn` helper for conditional classes
- Implement dark mode support from the start
- Test on real devices, not just browser DevTools

## 6. Project Structure Best Practices

### Decision
Use feature-based organization in both frontend and backend, with clear separation of concerns.

### Rationale
- Feature-based structure scales better than layer-based
- Clear separation makes it easy to find related code
- Aligns with domain-driven design principles
- Easy to add new features without impacting existing code

### Frontend Structure
```
src/
├── app/              # Next.js App Router pages
├── components/       # Reusable UI components
│   ├── auth/        # Auth-specific components
│   ├── tasks/       # Task-specific components
│   └── ui/          # Generic UI primitives
├── lib/             # Utilities and configurations
│   ├── auth.ts      # Better Auth config
│   ├── api-client.ts
│   └── types.ts
└── styles/          # Global styles
```

### Backend Structure
```
src/
├── main.py          # FastAPI app entry
├── models/          # SQLModel definitions
├── api/             # Route handlers
├── services/        # Business logic
├── middleware/      # Request/response middleware
└── database/        # DB connection and utilities
```

## Summary of Key Decisions

| Technology | Choice | Why |
|------------|--------|-----|
| Frontend Framework | Next.js 16+ App Router | Constitution requirement, modern React patterns |
| Authentication | Better Auth v1.x | Built for Next.js, handles JWT automatically |
| Backend Framework | FastAPI | Constitution requirement, fast and modern |
| ORM | SQLModel | Pydantic integration, type-safe |
| Database | Neon PostgreSQL | Constitution requirement, serverless |
| JWT Library | python-jose | FastAPI recommended, full-featured |
| API Communication | Native fetch | No extra deps, sufficient for needs |
| CSS Framework | TailwindCSS | Utility-first, responsive, popular |
| Design Approach | Mobile-first | Better UX on all devices |

## Next Steps

1. Create data-model.md with User and Task entities
2. Create API contracts in contracts/ directory
3. Create quickstart.md with setup instructions
4. Update agent context with technology decisions
5. Proceed to task generation (/sp.tasks)
