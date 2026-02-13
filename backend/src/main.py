"""FastAPI application for Todo App - Constitution compliant"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .api.health import router as health_router
from .api.tasks import router as tasks_router
from .api.auth import router as auth_router
from .api.users import router as users_router
from .api.admin import router as admin_router
from .database.connection import init_db

# Get FRONTEND_URL from environment for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Create FastAPI application
app = FastAPI(
    title="Todo App API",
    description="Secure multi-user todo application with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS - Allow frontend origin only
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:3000",  # Development fallback
        "https://*.vercel.app",  # Vercel deployments
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"]
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        print("Initializing database...")
        init_db()
        print("[OK] Database initialized successfully")
    except Exception as e:
        print(f"[WARNING] Database initialization warning: {e}")
        print("Tables may already exist or DATABASE_URL may not be set")


# Include routers
app.include_router(health_router)  # /health
app.include_router(auth_router)    # /auth/*
app.include_router(users_router)   # /users/*
app.include_router(tasks_router)   # /api/tasks/*
app.include_router(admin_router)   # /admin/* (for database inspection)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Todo App API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
