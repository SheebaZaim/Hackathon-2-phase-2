---
title: Todo App Backend
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Todo App Backend API

FastAPI backend for the Todo App with user authentication and task management.

## Features

- 🔐 User authentication with JWT
- ✅ Task CRUD operations
- 🗄️ PostgreSQL database (Neon)
- 📚 Auto-generated API documentation

## API Documentation

Once deployed, visit:
- `/docs` - Swagger UI
- `/redoc` - ReDoc
- `/health` - Health check endpoint

## Environment Variables

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT tokens

## Tech Stack

- FastAPI
- SQLModel (ORM)
- PostgreSQL (Neon)
- Python 3.11
