# Todo App - Full Stack Application

A modern, full-stack Todo application with user authentication, task management, and a clean UI. Built with Next.js, FastAPI, and PostgreSQL (Neon).

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11 or 3.12
- **PostgreSQL** database (Neon recommended)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd from-phase-2
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file with your database connection
# DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require
# BETTER_AUTH_SECRET=your-secret-key-here

# Run database migrations (if needed)
cd migrations
python run_migration.py 001_fix_users_table_nullable_fields.sql
cd ..

# Start backend server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: **http://localhost:8000**

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
# NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Start frontend server
npm run dev
```

Frontend will run on: **http://localhost:3000**

## 📋 Features

### Authentication
- ✅ User registration with email/password
- ✅ Secure login with JWT tokens
- ✅ Password hashing (SHA-256)
- ✅ Protected routes
- ✅ Multi-user support (each user sees only their tasks)

### Task Management
- ✅ Create tasks with title, description, priority, due date, category
- ✅ Mark tasks as complete/incomplete
- ✅ Edit task details
- ✅ Delete tasks
- ✅ Filter tasks (All/Active/Completed)
- ✅ Task persistence in PostgreSQL database

### UI/UX
- ✅ Clean, responsive design
- ✅ Real-time updates
- ✅ Form validation
- ✅ Error handling with user-friendly messages
- ✅ Loading states

## 🏗️ Tech Stack

### Frontend
- **Framework:** Next.js 14+ (React 18)
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Language:** TypeScript

### Backend
- **Framework:** FastAPI
- **ORM:** SQLModel
- **Database:** PostgreSQL (Neon)
- **Authentication:** JWT (python-jose)
- **Language:** Python 3.11+

### Database
- **Provider:** Neon (PostgreSQL)
- **Tables:** users, tasks
- **Features:** UUID primary keys, timestamps, foreign keys

## 📁 Project Structure

```
from-phase-2/
├── .agents/              # AI agent configurations
├── .claude/              # Claude Code settings
├── .qwen/                # Qwen AI configurations
├── .spec-kit/            # Spec-Kit configurations
├── backend/              # FastAPI backend
│   ├── migrations/       # Database migrations
│   ├── src/
│   │   ├── api/          # API endpoints (auth, tasks)
│   │   ├── models/       # SQLModel definitions
│   │   ├── middleware/   # Auth middleware
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   └── .env              # Database connection (not in git)
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/          # Pages (dashboard, login, register)
│   │   ├── components/   # React components (tasks)
│   │   └── lib/          # API client, types
│   ├── package.json
│   └── .env.local        # Backend URL (not in git)
├── specs/                # Specifications
│   ├── features/         # Feature specs
│   ├── api/              # API specs
│   ├── database/         # Database specs
│   └── ui/               # UI specs
├── history/              # Project history
├── plans/                # Planning documents
├── tasks/                # Task tracking
└── README.md             # This file
```

## 🔧 Configuration

### Backend Environment (.env)

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters
```

### Frontend Environment (.env.local)

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 🗄️ Database Schema

### Users Table
- `id` (UUID, primary key)
- `email` (string, unique)
- `first_name` (string, nullable)
- `last_name` (string, nullable)
- `password_hash` (string)
- `created_at` (timestamp)
- `updated_at` (timestamp)

### Tasks Table
- `id` (UUID, primary key)
- `user_id` (UUID, foreign key → users.id)
- `title` (string, max 255)
- `description` (text, nullable)
- `completed` (boolean, default false)
- `priority` (string: low/medium/high)
- `due_date` (datetime, nullable)
- `category` (string, nullable)
- `created_at` (timestamp)
- `updated_at` (timestamp)

## 🧪 Testing

### Backend Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T12:00:00",
  "database": "connected"
}
```

### Test Registration
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Test Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Full UI Test Flow
1. Open http://localhost:3000
2. Click "Get Started"
3. Register with email/password
4. Create a new task
5. Test complete/edit/delete
6. Test filters
7. Logout and login again

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔐 Security

- Passwords are hashed using SHA-256
- JWT tokens for authentication
- CORS configured for localhost:3000
- Database connections use SSL
- Environment variables for sensitive data
- SQL injection protection via SQLModel

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.11+)
- Verify DATABASE_URL in .env
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Check Node version: `node --version` (should be 18+)
- Install dependencies: `npm install`
- Verify NEXT_PUBLIC_BACKEND_URL in .env.local

### Database connection errors
- Verify DATABASE_URL format
- Check Neon project is active
- Test connection: `psql "your-database-url"`

### 401 Unauthorized errors
- Clear browser localStorage
- Re-register/login
- Check JWT token in browser DevTools → Application → Local Storage

### Tasks not loading
- Check backend is running on port 8000
- Check browser console for errors
- Verify auth token exists in localStorage

## 🚢 Deployment

### Backend (Railway, Render, Fly.io)
1. Set environment variables (DATABASE_URL, BETTER_AUTH_SECRET)
2. Deploy from backend/ directory
3. Use: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel, Netlify)
1. Set NEXT_PUBLIC_BACKEND_URL to your backend URL
2. Deploy from frontend/ directory
3. Build command: `npm run build`
4. Output directory: `.next`

### Database (Neon)
- Already hosted on Neon
- No additional deployment needed
- Use connection string in backend .env

## 📖 Documentation

- **Specifications:** `/specs` - Feature and API specifications
- **Status Files:** Root directory - CURRENT_STATUS.md, FIXES_APPLIED.md, etc.
- **Plans:** `/plans` - Implementation plans
- **History:** `/history` - Project development history

## 🤝 Contributing

1. Read specifications in `/specs`
2. Check current status in status files
3. Follow existing code structure
4. Test before committing
5. Update relevant documentation

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

- Your Name/Team

## 🙏 Acknowledgments

- Built with Next.js, FastAPI, and Neon
- Spec-driven development using GitHub Spec-Kit
- AI-assisted development with Claude Code

---

**Need help?** Check status files in root directory or specifications in `/specs`

**Quick Commands:**
```bash
# Start backend

cd backend && python -m uvicorn src.main:app --reload

# Start frontend
cd frontend && npm run dev

# Run migrations
cd backend/migrations && python run_migration.py <migration-file.sql>
```
