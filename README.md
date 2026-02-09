# Todo App - Phase II

A secure multi-user full-stack web application for managing personal todo tasks. Built following spec-driven development methodology with constitution-compliant architecture.

## Features

- **Secure Authentication**: Better Auth + JWT token-based authentication
- **Multi-User Support**: Each user has their own isolated task list
- **Task Management**: Create, update, complete, and delete tasks
- **Responsive Design**: Clean, simple UI that works on mobile, tablet, and desktop
- **Real-time Updates**: Modern React-based frontend with Next.js 16+
- **RESTful API**: Stateless backend with FastAPI and auto-generated API documentation

## Tech Stack (Constitution-Compliant)

- **Frontend**: Next.js 16+ (App Router), React, Better Auth, TailwindCSS
- **Backend**: Python FastAPI, SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (frontend) + JWT verification (backend)
- **Architecture**: Separate frontend/backend services, stateless authentication

## Project Structure

```
├── frontend/                # Next.js 16+ application
│   ├── src/
│   │   ├── app/            # Next.js App Router pages
│   │   ├── components/     # React UI components
│   │   ├── lib/            # Utilities (auth, API client, types)
│   │   └── styles/         # TailwindCSS global styles
│   ├── .env.example        # Frontend environment template
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── src/
│   │   ├── api/            # API route handlers
│   │   ├── models/         # SQLModel database models
│   │   ├── services/       # Business logic layer
│   │   ├── middleware/     # JWT authentication middleware
│   │   └── database/       # Database connection
│   ├── .env.example        # Backend environment template
│   └── requirements.txt
│
├── specs/                   # Feature specifications
│   ├── sp.constitution.md  # Project constitution (architectural rules)
│   └── */                  # Feature-specific specs, plans, tasks
│
└── README.md               # This file
```

## Quick Start (<10 minutes)

### Prerequisites

- Node.js 18+
- Python 3.11+
- npm or pnpm
- Neon PostgreSQL account (free tier available)

### 1. Install Dependencies

```bash
# Frontend
cd frontend
npm install
cd ..

# Backend
cd backend
pip install -r requirements.txt
cd ..
```

### 2. Configure Environment Variables

#### Frontend (.env)

```bash
cd frontend
cp .env.example .env
```

Edit `frontend/.env`:
```
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=<generate-with-openssl-rand-hex-32>
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend (.env)

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:
```
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=<same-secret-as-frontend>
FRONTEND_URL=http://localhost:3000
```

**⚠️ CRITICAL**: `BETTER_AUTH_SECRET` must be identical in both .env files!

### 3. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn src.main:app --reload
# Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

### 4. Verify Setup

- Frontend: http://localhost:3000 (should show authentication screen)
- Backend Health: http://localhost:8000/health
- API Docs: http://localhost:8000/docs (auto-generated Swagger UI)

## API Endpoints

### Health
- `GET /health` - Service health check with database status

### Tasks (requires authentication)
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task (title, description, completed status)
- `DELETE /api/tasks/{id}` - Delete task

All task endpoints require JWT token in `Authorization: Bearer <token>` header.

## Architecture

### Authentication Flow

1. **User Registration/Login**: Handled by Better Auth on frontend
2. **JWT Token Generation**: Better Auth issues JWT token on successful auth
3. **Token Storage**: Stored securely in httpOnly cookies
4. **API Requests**: Frontend attaches JWT to Authorization header
5. **Backend Verification**: FastAPI middleware verifies JWT using shared secret
6. **User Context**: Extracted from valid JWT for data isolation

### Data Isolation

- Each user's tasks are completely isolated
- Backend filters all queries by `user_id` from JWT payload
- No cross-user data access possible

### Constitution Compliance

This project strictly follows architectural rules defined in `specs/sp.constitution.md`:

✅ Fixed technology stack (no deviations allowed)
✅ Frontend and backend as separate services
✅ Stateless backend (JWT-only, no server sessions)
✅ Better Auth on frontend only
✅ RESTful APIs with proper error handling
✅ Spec-driven development (all code from specifications)

## Development

### Workflow

1. All features start with specifications in `/specs`
2. Specifications → Implementation plans → Tasks
3. Tasks executed following dependency order
4. Constitution compliance verified throughout

### Testing

- Frontend: Manual testing (run dev server, verify UI)
- Backend: Manual testing (health check, API docs)
- Integration: End-to-end user flows (signup → create task → logout)

### Environment Variables

See `.env.example` files in frontend/ and backend/ for complete variable documentation.

**Required Variables:**
- `DATABASE_URL`: Neon PostgreSQL connection (must include `?sslmode=require`)
- `BETTER_AUTH_SECRET`: Shared secret for JWT (min 32 chars)
- `NEXT_PUBLIC_API_URL`: Backend API URL (frontend)
- `FRONTEND_URL`: Frontend URL for CORS (backend)

## Troubleshooting

**Port conflicts:**
```bash
# Backend (default 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (default 3000)
lsof -ti:3000 | xargs kill -9
```

**Database connection:**
- Verify DATABASE_URL includes `?sslmode=require`
- Check Neon database is not paused (auto-pauses after inactivity)

**Authentication errors:**
- Ensure BETTER_AUTH_SECRET matches in both .env files
- Check JWT token is in Authorization header: `Bearer <token>`

**CORS errors:**
- Verify FRONTEND_URL in backend .env matches frontend URL
- Check backend CORS middleware allows frontend origin

## Contributing

1. Follow spec-driven development approach
2. All changes must originate from specifications
3. Verify constitution compliance before committing
4. Use feature branches: `###-feature-name`
5. Test locally before pushing

## License

MIT License - See LICENSE file for details

---

**Project Status**: Phase II - Cleanup and Functional Setup Complete
**Constitution Version**: 1.0.0
**Last Updated**: 2026-02-09
