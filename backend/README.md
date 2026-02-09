# Todo App Backend

This is the backend implementation for the Todo App Phase II project, built with FastAPI and SQLModel.

## Features

- **Authentication**: JWT-based authentication with user registration and login
- **Task Management**: Full CRUD operations for user tasks with ownership validation
- **Data Isolation**: Users can only access their own tasks
- **Security**: Password hashing, JWT validation, and proper error handling
- **Database**: PostgreSQL with SQLModel ORM

## Architecture

The backend follows the requirements specified in the project constitution and spec files:

- Built with Python FastAPI framework
- Uses SQLModel for ORM and database interactions
- Implements JWT-based authentication with shared secret
- Follows REST API conventions with proper authentication
- Enforces user ownership validation on all operations

## Key Components

- `main.py`: FastAPI application entry point with CORS configuration
- `db.py`: Database connection and session management
- `models/`: SQLModel database models for User and Task entities
- `middleware/jwt_middleware.py`: JWT token creation and validation
- `services/`: Business logic for authentication and task management
- `api/`: API route handlers for auth, tasks, and user endpoints

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate user and return JWT token
- `POST /api/auth/logout` - Logout user

### Tasks
- `GET /api/tasks` - Get all tasks for the current user
- `POST /api/tasks` - Create a new task for the current user
- `GET /api/tasks/{id}` - Get a specific task by ID
- `PUT /api/tasks/{id}` - Update a specific task (includes toggle functionality)
- `DELETE /api/tasks/{id}` - Delete a specific task

### User
- `GET /api/users/profile` - Get current user's profile information

## Environment Variables

Create a `.env` file with the following variables:

```bash
DATABASE_URL="postgresql://username:password@localhost:5432/todo_app"
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here-make-it-long-and-random"
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`

3. Initialize the database:
```bash
python init_db.py
```

4. Run the application:
```bash
cd src
uvicorn main:app --reload
```

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens with configurable expiration
- User ownership validation on all operations
- Input validation and sanitization
- Proper error handling without information disclosure

## Database Schema

### User Table
- `id`: UUID (Primary Key)
- `email`: String (Unique)
- `password_hash`: String
- `created_at`: DateTime
- `updated_at`: DateTime

### Task Table
- `id`: UUID (Primary Key)
- `title`: String
- `description`: String (Optional)
- `completed`: Boolean (Default: False)
- `user_id`: UUID (Foreign Key to User)
- `created_at`: DateTime
- `updated_at`: DateTime