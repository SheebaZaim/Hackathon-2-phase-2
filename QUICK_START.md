# ⚡ Quick Start - Todo App

## TL;DR - Get Running in 2 Minutes

### 1. Fix Database (one-time setup)
```bash
cd backend/migrations
python run_migration.py 001_fix_users_table_nullable_fields.sql
```

### 2. Test It Works
```bash
python test_registration.py
```

### 3. Use Your App
- Open http://localhost:3000
- Click "Get Started"
- Register with any email/password
- Start creating tasks!

---

## What's Already Running

✅ Backend: http://localhost:8000 (FastAPI)
✅ Frontend: http://localhost:3000 (Next.js)

Check health: `curl http://localhost:8000/health`

---

## Project Structure

```
from-phase-2/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── auth.py        ← Registration & Login
│   │   │   └── tasks.py       ← Task CRUD
│   │   ├── models/
│   │   │   ├── user.py        ← User model
│   │   │   └── task.py        ← Task model
│   │   └── main.py            ← FastAPI app
│   └── migrations/
│       ├── 001_fix_users_table_nullable_fields.sql
│       ├── run_migration.py   ← Run this first!
│       ├── test_registration.py
│       └── README.md
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── page.tsx         ← Homepage
    │   │   ├── login/page.tsx   ← Login page
    │   │   ├── register/page.tsx ← Register page
    │   │   └── dashboard/page.tsx ← Task dashboard
    │   ├── components/tasks/
    │   │   ├── TaskList.tsx
    │   │   ├── TaskItem.tsx
    │   │   ├── TaskForm.tsx
    │   │   └── TaskFilter.tsx
    │   └── lib/
    │       ├── api-client.ts    ← Backend API calls
    │       ├── auth-simple.ts   ← Auth functions
    │       └── types.ts         ← TypeScript types
    └── package.json
```

---

## Key Features

- 🔐 **Authentication**: Email/password with JWT tokens
- ✅ **Task Management**: Create, edit, delete, complete tasks
- 🎯 **Filtering**: View All, Active, or Completed tasks
- 👥 **Multi-user**: Each user sees only their own tasks
- 🎨 **Clean UI**: Simple, responsive design
- 🔒 **Secure**: SHA-256 password hashing, JWT authentication

---

## API Endpoints

**Auth**:
- `POST /auth/register` - Create account
- `POST /auth/login` - Sign in

**Tasks** (requires JWT token):
- `GET /api/tasks` - List tasks (optional: ?completed=true/false)
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

**Health**:
- `GET /health` - Check backend status

Docs: http://localhost:8000/docs

---

## Common Commands

**Backend**:
```bash
# Start backend
cd backend
backend_env_py311/Scripts/python.exe -m uvicorn src.main:app --reload

# Run migration
cd migrations
python run_migration.py 001_fix_users_table_nullable_fields.sql

# Test registration
python test_registration.py
```

**Frontend**:
```bash
# Start frontend
cd frontend
npm run dev

# Build for production
npm run build
```

**Both**:
```bash
# Health check
curl http://localhost:8000/health

# Test registration
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'
```

---

## Need Help?

- **Detailed guide**: See `NEXT_STEPS.md`
- **Testing guide**: See `TESTING.md`
- **Current status**: See `CURRENT_STATUS.md`
- **Migration help**: See `backend/migrations/README.md`

---

**That's all you need to know!** Run the migration and start using your app. 🎉
