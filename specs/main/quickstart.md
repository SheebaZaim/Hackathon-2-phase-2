# Quickstart Guide: Todo App Phase II

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- Neon PostgreSQL account
- Better Auth account (or self-hosted)

## Environment Setup
1. Clone the repository
2. Create `.env` files in both `backend/` and `frontend/` directories
3. Configure the following environment variables:

### Backend (.env)
```env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname"
BETTER_AUTH_SECRET="your-jwt-secret-key-here"
```

### Frontend (.env)
```env
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
BETTER_AUTH_SECRET="same-jwt-secret-key-as-backend"
```

## Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m src.main  # To initialize database
uvicorn src.main:app --reload  # Start backend server
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Start frontend server
```

## Running the Application
1. Start the backend server first
2. Start the frontend server
3. Navigate to http://localhost:3000 in your browser
4. Register a new account or log in to existing account
5. Begin creating and managing your tasks

## API Endpoints
- Authentication: POST /api/auth/login, POST /api/auth/register
- Tasks: GET/POST/PUT/DELETE /api/tasks
- User Profile: GET /api/users/profile

## Troubleshooting
- Ensure both backend and frontend servers are running
- Verify environment variables are properly set
- Check that Neon PostgreSQL connection string is correct
- Confirm JWT secrets match between frontend and backend