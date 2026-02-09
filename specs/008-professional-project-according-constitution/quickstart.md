# Quickstart Guide: Professional Project According to Constitution

## Overview
This guide provides instructions for setting up and running the professional project according to the constitution. The project implements a secure multi-user todo application using the mandated technology stack.

## Prerequisites
- Node.js 18+ and npm/yarn for the frontend
- Python 3.11+ for the backend
- PostgreSQL client tools
- Git
- A Neon Serverless PostgreSQL account
- A code editor (VS Code recommended)

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup (Python FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```env
   DATABASE_URL=your_neon_database_url
   BETTER_AUTH_SECRET=your_jwt_secret_key
   BETTER_AUTH_URL=http://localhost:3000
   ```

### 3. Frontend Setup (Next.js)
1. Navigate to the frontend directory:
   ```bash
   cd frontend  # or cd ../frontend if you're in the backend directory
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables by creating a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXTAUTH_SECRET=your_nextauth_secret
   NEXTAUTH_URL=http://localhost:3000
   ```

## Running the Application

### 1. Starting the Backend
1. Ensure you're in the backend directory
2. Activate your virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Run the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### 2. Starting the Frontend
1. Ensure you're in the frontend directory
2. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
3. Visit `http://localhost:3000` in your browser

## Database Setup
1. Ensure your Neon Serverless PostgreSQL database is created
2. Run the database migrations:
   ```bash
   # From the backend directory
   python -m src.database.migrate
   ```

## API Documentation
Once the backend is running, API documentation is available at:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Authentication Flow (Constitution Compliant)
1. Register a new user via Better Auth on the frontend
2. Upon successful registration/login, JWT tokens are issued and stored securely
3. JWT tokens must be attached to the Authorization header for all authenticated requests to the backend:
   ```
   Authorization: Bearer {your-jwt-token}
   ```
4. The backend verifies JWT tokens using the shared secret via BETTER_AUTH_SECRET environment variable

## Key Features
- User registration and authentication
- Creating and managing todo lists
- Adding, updating, and completing tasks
- Cross-device synchronization
- Secure data isolation between users

## Troubleshooting
- If you encounter database connection issues, verify your Neon database URL and credentials
- If authentication fails, ensure the `BETTER_AUTH_SECRET` matches between frontend and backend
- For frontend build issues, try clearing the cache: `npm run clean` or deleting the `.next` directory

## Constitution Compliance Verification
Verify that the implementation follows all constitution requirements:

**Technology Stack Compliance**:
- [ ] Frontend: Next.js 16+ (App Router) - CONFIRMED
- [ ] Backend: Python FastAPI - CONFIRMED
- [ ] ORM: SQLModel - CONFIRMED
- [ ] Database: Neon Serverless PostgreSQL - CONFIRMED
- [ ] Authentication: Better Auth + JWT - CONFIRMED

**Architecture Constraints**:
- [ ] Frontend and backend as separate services - CONFIRMED
- [ ] Stateless backend for authentication - CONFIRMED
- [ ] JWT as only authentication mechanism between services - CONFIRMED
- [ ] RESTful APIs with proper error handling - CONFIRMED

**Security Rules**:
- [ ] Better Auth on frontend only - CONFIRMED
- [ ] JWT tokens with secure storage - CONFIRMED
- [ ] Authorization header for authenticated requests - CONFIRMED
- [ ] Shared secret verification via BETTER_AUTH_SECRET - CONFIRMED
- [ ] Encryption at rest and in transit - CONFIRMED
- [ ] Stateless session management - CONFIRMED

## Next Steps
1. Explore the API endpoints using the interactive documentation
2. Customize the UI components in the `frontend/src/components` directory
3. Extend the data model by modifying the SQLModel definitions
4. Add new API endpoints following the existing patterns