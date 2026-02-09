from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth_router import router as auth_router
from .api.class_router import router as class_router
from .api.student_router import router as student_router
from .api.subject_router import router as subject_router
from .api.result_router import router as result_router
from .config.settings import settings
from .db import create_db_engine
from sqlmodel import SQLModel
import os


# Create engine with SSL support for Neon
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
engine = create_db_engine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to create tables on startup"""
    # Import all models to register them with SQLModel metadata
    # Note: Due to compatibility issues, models are imported inside the lifespan function
    try:
        from .models.user_model import User
        from .models.class_model import Class
        from .models.student_model import Student
        from .models.subject_model import Subject
        from .models.result_model import Result

        print("Creating tables...")
        SQLModel.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

    yield
    # Perform any cleanup on shutdown if needed


# Create FastAPI application instance
app = FastAPI(
    title="Teacher Planning App Backend",
    description="A secure multi-user application for teachers to manage school plannings, student results, and task lists",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to allow JWT tokens to be read by frontend
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Include API routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(class_router, prefix="/api/v1/classes", tags=["classes"])
app.include_router(student_router, prefix="/api/v1/students", tags=["students"])
app.include_router(subject_router, prefix="/api/v1/subjects", tags=["subjects"])
app.include_router(result_router, prefix="/api/v1/results", tags=["results"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "teacher-planning-backend"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Teacher Planning App Backend"}