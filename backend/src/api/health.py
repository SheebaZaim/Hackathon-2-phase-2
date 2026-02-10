"""Health check endpoint for Todo App"""
from fastapi import APIRouter, Depends
from sqlmodel import Session
from datetime import datetime

from ..database.connection import get_session, test_connection

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns service status and database connectivity.
    No authentication required.
    """
    db_status = "connected" if test_connection() else "disconnected"

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status
    }
