"""Admin API endpoints for database inspection (development only)"""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List, Dict, Any

from ..models.task import Task
from ..models.user import User
from ..database.connection import get_session

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def get_database_stats(session: Session = Depends(get_session)) -> Dict[str, Any]:
    """Get database statistics"""

    # Count users
    user_count = len(session.exec(select(User)).all())

    # Count tasks
    task_count = len(session.exec(select(Task)).all())

    # Count completed tasks
    completed_count = len(session.exec(select(Task).where(Task.completed == True)).all())

    # Count by priority
    priority_stats = {}
    for priority in ['low', 'medium', 'high']:
        count = len(session.exec(select(Task).where(Task.priority == priority)).all())
        priority_stats[priority] = count

    return {
        "total_users": user_count,
        "total_tasks": task_count,
        "completed_tasks": completed_count,
        "active_tasks": task_count - completed_count,
        "priority_breakdown": priority_stats
    }


@router.get("/users")
async def get_all_users(session: Session = Depends(get_session)) -> List[Dict[str, Any]]:
    """Get all users (without passwords)"""
    users = session.exec(select(User)).all()

    return [
        {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": str(user.created_at),
        }
        for user in users
    ]


@router.get("/tasks")
async def get_all_tasks(session: Session = Depends(get_session)) -> List[Dict[str, Any]]:
    """Get all tasks from all users"""
    tasks = session.exec(select(Task)).all()

    return [
        {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": str(task.due_date) if task.due_date else None,
            "category": task.category,
            "created_at": str(task.created_at),
        }
        for task in tasks
    ]


@router.get("/tasks/by-user/{email}")
async def get_tasks_by_user_email(
    email: str,
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """Get all tasks for a specific user by email"""

    # Find user by email
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        return {"error": "User not found", "email": email}

    # Get user's tasks
    tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()

    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
        },
        "task_count": len(tasks),
        "tasks": [
            {
                "id": str(task.id),
                "title": task.title,
                "completed": task.completed,
                "priority": task.priority,
                "due_date": str(task.due_date) if task.due_date else None,
                "category": task.category,
            }
            for task in tasks
        ]
    }
