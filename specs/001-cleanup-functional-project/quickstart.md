# Quickstart Guide: Todo App Setup

**Feature**: 001-cleanup-functional-project
**Date**: 2026-02-09
**Target Time**: <10 minutes from zero to running application

## Prerequisites

Before you begin, ensure you have the following installed:

- ✅ **Node.js 18+** (check: `node --version`)
- ✅ **Python 3.11+** (check: `python --version`)
- ✅ **Git** (check: `git --version`)
- ✅ **npm or pnpm** (check: `npm --version`)
- ✅ **pip** (check: `pip --version`)

## Quick Start (5 Steps)

### Step 1: Clone and Setup (1 minute)

```bash
# Clone the repository
git clone <repository-url>
cd todo-app

# Install frontend dependencies
cd frontend
npm install  # or: pnpm install
cd ..

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### Step 2: Create Neon Database (2 minutes)

1. Go to [https://console.neon.tech](https://console.neon.tech)
2. Sign up or login
3. Create a new project: "todo-app"
4. Copy the connection string (format: `postgresql://user:pass@host/db?sslmode=require`)

### Step 3: Configure Environment Variables (2 minutes)

#### Frontend Environment

```bash
cd frontend
cp .env.example .env
```

Edit `frontend/.env`:
```bash
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Authentication Secret (generate with: openssl rand -hex 32)
BETTER_AUTH_SECRET=your-random-secret-here-min-32-chars

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend Environment

```bash
cd ../backend
cp .env.example .env
```

Edit `backend/.env`:
```bash
# Database (Neon PostgreSQL) - SAME as frontend
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Authentication Secret - MUST match frontend
BETTER_AUTH_SECRET=your-random-secret-here-min-32-chars

# CORS - Frontend URL
FRONTEND_URL=http://localhost:3000
```

**⚠️ IMPORTANT**: `BETTER_AUTH_SECRET` must be identical in both frontend and backend!

### Step 4: Initialize Database (1 minute)

The database tables will be created automatically when you start the backend for the first time, or you can run:

```bash
cd backend
python -m src.database.init_db
```

### Step 5: Start Both Services (1 minute)

#### Terminal 1 - Backend

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

You should see:
```
  ▲ Next.js 16.x.x
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

### Step 6: Verify Setup (1 minute)

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```
   Expected: `{"status":"healthy","database":"connected"}`

2. **Frontend**:
   Open browser to [http://localhost:3000](http://localhost:3000)
   Expected: Authentication screen (signin/signup)

3. **API Documentation**:
   Open browser to [http://localhost:8000/docs](http://localhost:8000/docs)
   Expected: Swagger UI with API endpoints

## Verification Checklist

After completing the setup, verify:

- [ ] Backend responds to http://localhost:8000/health
- [ ] Frontend loads at http://localhost:3000
- [ ] You can see signup/signin forms
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] No errors in backend terminal
- [ ] No errors in frontend terminal

## Troubleshooting

### Backend won't start

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

**Problem**: `Connection to database failed`
**Solution**:
- Verify DATABASE_URL is correct
- Ensure `?sslmode=require` is at the end of the URL
- Check Neon database is active (not paused)

**Problem**: `Port 8000 already in use`
**Solution**:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows, then taskkill /PID <pid> /F
# Or use different port:
uvicorn src.main:app --reload --port 8001
```

### Frontend won't start

**Problem**: `Error: Cannot find module 'next'`
**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: `Port 3000 already in use`
**Solution**:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9  # Mac/Linux
# Or Next.js will automatically suggest port 3001
```

**Problem**: `BETTER_AUTH_SECRET not defined`
**Solution**:
- Ensure .env file exists in frontend directory
- Verify BETTER_AUTH_SECRET is set
- Restart frontend dev server

### Authentication not working

**Problem**: "Could not validate credentials" when making API requests
**Solution**:
- Verify BETTER_AUTH_SECRET is IDENTICAL in frontend and backend .env files
- Check token is being sent in Authorization header
- Verify backend is running and accessible

**Problem**: CORS errors in browser console
**Solution**:
- Verify FRONTEND_URL in backend .env matches frontend URL
- Check backend CORS middleware is configured
- Ensure cookies are allowed (credentials: true)

### Database issues

**Problem**: "relation 'users' does not exist"
**Solution**:
```bash
cd backend
python -m src.database.init_db
```

**Problem**: "SSL connection required"
**Solution**:
- Add `?sslmode=require` to DATABASE_URL
- Neon requires SSL for all connections

## Development Workflow

### Making Changes

1. **Frontend changes**: Auto-reload enabled (save file to see changes)
2. **Backend changes**: Auto-reload enabled with `--reload` flag
3. **Database schema changes**: Run migration script (if added)
4. **Environment variable changes**: Restart respective service

### Running in Production

```bash
# Frontend (build and start)
cd frontend
npm run build
npm start

# Backend (use production ASGI server)
cd backend
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Next Steps

Once the application is running:

1. ✅ **Test signup**: Create a new user account
2. ✅ **Test signin**: Login with created account
3. ✅ **Test tasks**: Create, update, complete, delete tasks
4. ✅ **Test logout**: Logout and verify you can't access tasks
5. ✅ **Test isolation**: Create second user, verify can't see first user's tasks

## Useful Commands

### Generate Secure Secret

```bash
# For BETTER_AUTH_SECRET
openssl rand -hex 32
```

### View Database Tables

```bash
# Using psql
psql $DATABASE_URL -c "\dt"

# Using Python
cd backend
python -c "from src.database.connection import engine; from sqlmodel import SQLModel; print(SQLModel.metadata.tables.keys())"
```

### Reset Database

```bash
cd backend
python -m src.database.reset_db  # Drops and recreates all tables
```

### Check Dependencies

```bash
# Frontend
cd frontend
npm list --depth=0

# Backend
cd backend
pip list
```

## Environment Variables Reference

### Frontend (.env)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| DATABASE_URL | Yes | Neon PostgreSQL connection string | `postgresql://user:pass@host/db?sslmode=require` |
| BETTER_AUTH_SECRET | Yes | Shared secret for JWT (min 32 chars) | `<output of openssl rand -hex 32>` |
| NEXT_PUBLIC_API_URL | Yes | Backend API base URL | `http://localhost:8000` |

### Backend (.env)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| DATABASE_URL | Yes | Neon PostgreSQL connection string | `postgresql://user:pass@host/db?sslmode=require` |
| BETTER_AUTH_SECRET | Yes | Shared secret for JWT (must match frontend) | `<same as frontend>` |
| FRONTEND_URL | Yes | Frontend base URL for CORS | `http://localhost:3000` |

## Support

If you encounter issues not covered here:

1. Check the [API documentation](http://localhost:8000/docs)
2. Review backend logs in terminal
3. Review frontend console in browser DevTools
4. Verify all environment variables are set correctly
5. Ensure both services are running on correct ports

## Success Criteria

You've successfully completed setup when:

- ✅ Backend starts in <2 seconds
- ✅ Frontend starts in <5 seconds
- ✅ You can signup and signin
- ✅ You can create, view, update, delete tasks
- ✅ Tasks are persisted in Neon database
- ✅ Multiple users have isolated task lists

**Total setup time**: Should be <10 minutes ⚡
