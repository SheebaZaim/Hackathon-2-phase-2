# Quickstart Guide: Teacher Planning App

## Overview
This guide provides instructions for setting up and running the Teacher Planning Application, a secure multi-user full-stack web application for teachers to manage school plannings, student results, and task lists.

## Prerequisites
- Node.js v18+ installed
- Python 3.11+ installed
- npm or yarn package manager
- Access to Neon PostgreSQL database
- Better Auth configured for frontend authentication

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Navigate to the Feature Branch
```bash
git checkout 005-teacher-planning-app
```

### 3. Set Up Backend
```bash
cd backend
pip install -r requirements.txt
```

### 4. Set Up Frontend
```bash
cd frontend
npm install
# or
yarn install
```

## Configuration

### 1. Backend Configuration
Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=your_neon_postgres_connection_string
BETTER_AUTH_SECRET=your_secure_jwt_secret
```

### 2. Frontend Configuration
Create a `.env.local` file in the `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Running the Applications

### 1. Start the Backend
```bash
cd backend
python -m src.main
# or using uvicorn
uvicorn src.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
# or
yarn dev
```

### 3. Access the Application
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Backend Documentation: `http://localhost:8000/docs`

## Key Features

### Authentication
- Register with email and password
- Login with existing credentials
- Secure JWT token management
- Protected routes for authorized users only
- Secure logout functionality
- Persistent navigation with logout button
- Prominent, intuitive login/register buttons with hover effects

### School Planning Management
- Create new school plannings (lesson plans, schedules, etc.)
- Edit existing plannings with teacher-specific fields (learning objectives, materials needed, class size, teaching methods, etc.)
- Delete unwanted plannings
- View all your plannings in a teacher-friendly interface
- Filter plannings by subject, grade level, or date
- Include educational standards addressed in each planning

### Student Results Management
- Create new student result entries with detailed information
- Upload student results in bulk (coming soon)
- Edit existing student results with comments and grades
- View student results in organized formats
- Track student progress over time
- Associate results with specific assignments and subjects

### Task Management
- Create new tasks with title, description, due date, category, and teacher-specific fields
- Mark tasks as complete/incomplete
- Edit or delete existing tasks
- Filter tasks by status, date, category, or subject area
- Set reminders and recurring tasks for regular activities
- Associate tasks with specific classes or students
- Track estimated vs. actual time spent on tasks

### UI/UX Improvements
- Clean, professional design with school-themed colors (blue, green)
- Properly sized and centered images that don't dominate the page
- Balanced grid layout avoiding extreme corner placements
- Dedicated columns/modals for editing with teacher-specific fields
- Mobile-responsive design for access on various devices
- Intuitive navigation with persistent menu
- Accessible design following WCAG guidelines

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login with credentials
- `POST /api/auth/logout` - Logout from the application

### School Plannings
- `GET /api/plannings` - Get all user's plannings
- `POST /api/plannings` - Create a new planning
- `GET /api/plannings/{id}` - Get a specific planning
- `PUT /api/plannings/{id}` - Update a planning
- `DELETE /api/plannings/{id}` - Delete a planning

### Student Results
- `GET /api/results` - Get all user's student results
- `POST /api/results` - Create a new student result
- `GET /api/results/{id}` - Get a specific result
- `PUT /api/results/{id}` - Update a result
- `DELETE /api/results/{id}` - Delete a result

### Tasks
- `GET /api/tasks` - Get all user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion status

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify your Neon PostgreSQL connection string is correct
- Check that your database is accessible
- Ensure you have the necessary permissions

#### Authentication Issues
- Verify that BETTER_AUTH_SECRET is the same in both frontend and backend
- Check that JWT tokens are being properly stored and sent with requests
- Ensure CORS settings allow frontend-backend communication

#### Frontend Build Issues
- Make sure all dependencies are installed
- Verify environment variables are properly set
- Check that the backend is running when accessing API endpoints

### Debugging Commands
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check database connection
python -c "from backend.src.db import engine; print('Connected to DB')" 

# Check frontend environment
npm run build
```

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
# or
yarn test
```

### Setting Up for Development
1. Install all dependencies
2. Set up your Neon PostgreSQL database
3. Configure environment variables
4. Run database migrations (if applicable)
5. Start both backend and frontend

## Security Considerations
- JWT tokens are stored securely in the browser
- All API requests are authenticated
- User data is isolated between accounts
- Passwords are properly hashed and salted
- Input validation prevents injection attacks