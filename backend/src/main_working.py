from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth_router import router as auth_router
from .api.school_planning_router import router as school_planning_router
from .api.student_result_router import router as student_result_router
from .api.task_router import router as task_router
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
    # Only attempt to create tables if we can import the models
    try:
        # Import models inside the lifespan function to avoid startup issues
        import importlib
        models_module = importlib.import_module(".models.user_model", package="src")
        User = models_module.User
        
        models_module = importlib.import_module(".models.task_model", package="src")
        Task = models_module.Task
        
        models_module = importlib.import_module(".models.school_planning_model", package="src")
        SchoolPlanning = models_module.SchoolPlanning
        
        models_module = importlib.import_module(".models.student_result_model", package="src")
        StudentResult = models_module.StudentResult
        
        models_module = importlib.import_module(".models.task_template", package="src")
        TaskTemplate = models_module.TaskTemplate
        
        print("Creating tables...")
        SQLModel.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Could not create tables: {e}")
        # Continue anyway to allow the app to start
    
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
    allow_origins=settings.allowed_origins,  # Fixed: was settings.ALLOWED_ORIGINS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to allow JWT tokens to be read by frontend
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Include API routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(school_planning_router, prefix="/api/v1/plannings", tags=["school-plannings"])
app.include_router(student_result_router, prefix="/api/v1/results", tags=["student-results"])
app.include_router(task_router, prefix="/api/v1/tasks", tags=["tasks"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "teacher-planning-backend"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Teacher Planning App Backend"}