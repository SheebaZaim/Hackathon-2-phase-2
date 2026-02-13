# Todo App Frontend - Setup Guide

## Overview

This guide helps you set up and run the Todo App frontend, which is built with Next.js 16, TypeScript, Better Auth, and integrates with the FastAPI backend.

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Backend server running at `http://localhost:8000`
- PostgreSQL database (Neon) accessible

## Installation Steps

### 1. Install Dependencies

```bash
cd frontend
npm install
```

If you encounter peer dependency conflicts, use:
```bash
npm install --legacy-peer-deps
```

### 2. Configure Environment Variables

Create `.env.local` file from the example:

```bash
cp .env.example .env.local
```

Edit `.env.local` with your configuration:

```env
# Backend API URL
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:3000

# Better Auth Secret (MUST match backend)
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long

# Better Auth URL
BETTER_AUTH_URL=http://localhost:3000

# Database Connection (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@your-neon-host/database?sslmode=require

# Environment
NODE_ENV=development
```

**IMPORTANT**:
- `BETTER_AUTH_SECRET` must be at least 32 characters
- `BETTER_AUTH_SECRET` MUST match the value in `backend/.env`
- `DATABASE_URL` should point to your Neon PostgreSQL database

### 3. Verify Backend is Running

Before starting the frontend, ensure the backend is running:

```bash
# In a separate terminal, from project root:
cd backend
backend_env_py311/Scripts/python.exe -m uvicorn src.main:app --reload
```

Test backend health:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-10T...",
  "database": "connected"
}
```

### 4. Start Development Server

```bash
npm run dev
```

The frontend will start at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── auth/
│   │   │       └── [...all]/route.ts    # Better Auth API handler
│   │   ├── dashboard/page.tsx           # Protected dashboard
│   │   ├── login/page.tsx               # Login page
│   │   ├── register/page.tsx            # Registration page
│   │   ├── layout.tsx                   # Root layout
│   │   └── page.tsx                     # Homepage
│   ├── components/
│   │   └── tasks/
│   │       ├── TaskListComponent.tsx    # Task list display
│   │       ├── TaskItemComponent.tsx    # Individual task
│   │       ├── TaskFormComponent.tsx    # Create task form
│   │       └── TaskFilter.tsx           # Filter buttons
│   ├── hooks/
│   │   └── useTasks.ts                  # Task CRUD hook
│   ├── lib/
│   │   ├── auth.ts                      # Better Auth server config
│   │   ├── auth-client.ts               # Better Auth client
│   │   ├── token-utils.ts               # JWT token utilities
│   │   ├── api-client.ts                # Backend API client
│   │   └── types.ts                     # TypeScript types
│   └── styles/
│       └── globals.css                  # Global styles
├── .env.example                         # Environment template
├── .env.local                           # Your local config (gitignored)
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## Key Technologies

### Better Auth
- **Version**: 1.5.0-beta.13
- **Purpose**: User authentication and session management
- **Configuration**: Server-side in `lib/auth.ts`, client-side in `lib/auth-client.ts`
- **Database**: Uses same Neon PostgreSQL as backend

### Backend Integration
- **API Client**: `lib/api-client.ts` handles all backend requests
- **JWT Tokens**: Automatically attached to requests via axios interceptors
- **Endpoints**: All 7 backend endpoints (health, task CRUD) are wrapped

### TypeScript
- **Strict Mode**: Enabled for type safety
- **Types**: Defined in `lib/types.ts` matching backend models
- **Components**: All new components use TypeScript

## Quick Start Workflow

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   backend_env_py311/Scripts/python.exe -m uvicorn src.main:app --reload
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**: Navigate to `http://localhost:3000`

4. **Register User**: Click "Get Started" and create an account

5. **Create Tasks**: Use the dashboard to create and manage tasks

## Common Issues

### Port Already in Use

If port 3000 is already in use:
```bash
# Kill the process on port 3000 (Windows)
npx kill-port 3000

# Or specify a different port
PORT=3001 npm run dev
```

### CORS Errors

If you see CORS errors in browser console:
- Verify backend is running
- Check backend CORS configuration allows `http://localhost:3000`
- Verify `NEXT_PUBLIC_BACKEND_URL` in `.env.local`

### Authentication Not Working

1. **Check Environment Variables**:
   - Verify `BETTER_AUTH_SECRET` is set and matches backend
   - Verify `DATABASE_URL` is correct

2. **Clear Browser Data**:
   ```javascript
   // In browser console:
   localStorage.clear();
   // Then refresh page
   ```

3. **Check Backend Logs**: Look for JWT verification errors

### Build Errors

TypeScript or build errors:
```bash
# Clear Next.js cache
rm -rf .next

# Rebuild
npm run build
```

### Database Connection Errors

If Better Auth can't connect to database:
- Verify `DATABASE_URL` is correct
- Check Neon dashboard for database status
- Ensure IP is whitelisted in Neon settings
- Test connection using psql or similar tool

## Development Tips

### Hot Reload
Next.js automatically reloads when you save files. If it stops working:
- Restart dev server
- Check for syntax errors in console

### TypeScript Errors
Run type checking:
```bash
npm run build
```

### Debugging
1. Open browser DevTools (F12)
2. Check Console for errors
3. Check Network tab for API requests
4. Verify Authorization header includes JWT token

### Testing API Calls
In browser console:
```javascript
// Get current token
localStorage.getItem('auth_token');

// Test health endpoint
fetch('http://localhost:8000/health').then(r => r.json()).then(console.log);

// Test tasks endpoint (requires auth)
fetch('http://localhost:8000/api/tasks', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
  }
}).then(r => r.json()).then(console.log);
```

## Production Build

### Build for Production
```bash
npm run build
```

### Run Production Server
```bash
npm start
```

### Deploy to Vercel
1. Connect GitHub repository to Vercel
2. Configure environment variables in Vercel dashboard
3. Deploy

**Production Environment Variables**:
- `NEXT_PUBLIC_BACKEND_URL`: Production backend URL
- `BETTER_AUTH_SECRET`: Same as backend (keep secret!)
- `DATABASE_URL`: Production Neon database
- `BETTER_AUTH_URL`: Production frontend URL

## Next Steps

After successful setup:
1. ✅ Register a test user
2. ✅ Create some tasks
3. ✅ Test all CRUD operations
4. ✅ Test filtering (All/Active/Completed)
5. ✅ Test responsive design
6. ✅ Review [TESTING.md](./TESTING.md) for comprehensive test checklist

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://better-auth.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Backend API Documentation](../backend/README.md)
- [Testing Guide](./TESTING.md)
- [Frontend Guidelines](./Frontend%20CLAUDE.md)

## Support

For issues or questions:
1. Check [TESTING.md](./TESTING.md) troubleshooting section
2. Review browser console for errors
3. Check backend logs for API errors
4. Verify environment variables are correct
