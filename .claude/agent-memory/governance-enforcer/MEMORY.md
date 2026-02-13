# Governance Enforcer Memory

## Project Structure
- **Monorepo**: Frontend (Next.js 14) + Backend (FastAPI + SQLModel + Neon PostgreSQL)
- **Constitution**: D:\from-phase-2\specs\sp.constitution.md
- **Key Specs**: Located in D:\from-phase-2\specs\008-professional-project-according-constitution\

## Constitutional Requirements
1. **Fixed Tech Stack**: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT
2. **Stateless Backend**: JWT-only authentication, no server-side sessions
3. **Separation**: Frontend/backend as separate services, no tight coupling
4. **Security**: BETTER_AUTH_SECRET shared, passwords hashed, JWT tokens in Authorization header
5. **Spec-Driven Dev**: All code must originate from specifications in /specs

## Current Implementation Status
- **Backend**: Uses simplified JWT auth (NOT Better Auth as required by constitution)
- **Frontend**: Direct backend integration via auth-simple.ts (bypasses Better Auth requirement)
- **API Structure**: Flat task API at /api/tasks (spec suggests /todo-lists/{id}/tasks structure)
- **Database**: PostgreSQL via Neon, properly configured with migrations

## Common Violations Found
1. **Better Auth Not Implemented**: Constitution requires Better Auth on frontend, but project uses direct backend auth
2. **API Structure Mismatch**: Implemented /api/tasks vs specified /todo-lists/{id}/tasks
3. **Missing Endpoints**: PATCH /tasks/{id}/toggle-completion, POST /auth/logout, GET /users/me
4. **Password Hashing**: Uses SHA-256 (weak) instead of bcrypt/argon2
5. **Missing .env.example**: No documented environment variables template

## Security Issues
- **Weak Password Hashing**: SHA-256 with static salt (backend/src/api/auth.py line 17)
- **Token Storage**: localStorage (should use httpOnly cookies per specs)
- **Missing HTTPS Enforcement**: No redirect or requirement in production config

## Architecture Patterns
- **Model Location**: backend/src/models/ (user.py, task.py)
- **API Location**: backend/src/api/ (auth.py, tasks.py, health.py, admin.py)
- **Middleware**: backend/src/middleware/auth.py (JWT verification)
- **Database**: backend/src/database/connection.py (SQLModel + Neon)

## Files to Check for Compliance
- Constitution: specs/sp.constitution.md
- API Contract: specs/008-professional-project-according-constitution/contracts/api-contracts.md
- Backend Auth: backend/src/api/auth.py
- Frontend Auth: frontend/src/lib/auth-simple.ts (should be using Better Auth)
- Middleware: backend/src/middleware/auth.py

## Remediation Patterns
1. **Better Auth Integration**: Install better-auth npm package, configure auth.ts, update frontend
2. **API Restructuring**: Add /todo-lists endpoints, nest tasks under lists
3. **Password Security**: Replace SHA-256 with bcrypt in backend
4. **Missing Endpoints**: Add PATCH toggle, logout, users/me endpoints
5. **Environment Templates**: Create comprehensive .env.example files
