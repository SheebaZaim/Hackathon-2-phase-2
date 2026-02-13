"""Task CRUD API endpoints for Todo App - per contracts/api-endpoints.yaml"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID

from ..models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from ..services.tasks import TaskService
from ..middleware.auth import get_current_user
from ..database.connection import get_session

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=dict)
async def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for authenticated user.
    Supports filtering by completion status and pagination.
    """
    user_id = auth_data["user_id"]

    tasks = TaskService.get_tasks(
        session=session,
        user_id=user_id,
        completed=completed,
        limit=limit,
        offset=offset
    )

    total = TaskService.count_tasks(
        session=session,
        user_id=user_id,
        completed=completed
    )

    # Convert to response format
    task_responses = [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            due_date=task.due_date,
            category=task.category,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]

    return {
        "tasks": task_responses,
        "total": total
    }


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user"""
    user_id = auth_data["user_id"]

    task = TaskService.create_task(
        session=session,
        user_id=user_id,
        task_data=task_data
    )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        due_date=task.due_date,
        category=task.category,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task (must belong to authenticated user)"""
    user_id = auth_data["user_id"]

    task = TaskService.get_task(
        session=session,
        user_id=user_id,
        task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        due_date=task.due_date,
        category=task.category,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a task (must belong to authenticated user)"""
    user_id = auth_data["user_id"]

    task = TaskService.update_task(
        session=session,
        user_id=user_id,
        task_id=task_id,
        task_data=task_data
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        due_date=task.due_date,
        category=task.category,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a task (must belong to authenticated user)"""
    user_id = auth_data["user_id"]

    deleted = TaskService.delete_task(
        session=session,
        user_id=user_id,
        task_id=task_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return None  # 204 No Content


@router.patch("/{task_id}/toggle-completion", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: UUID,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle task completion status (must belong to authenticated user)"""
    user_id = auth_data["user_id"]

    # Get current task
    task = TaskService.get_task(
        session=session,
        user_id=user_id,
        task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion
    task_data = TaskUpdate(completed=not task.completed)
    updated_task = TaskService.update_task(
        session=session,
        user_id=user_id,
        task_id=task_id,
        task_data=task_data
    )

    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        priority=updated_task.priority,
        due_date=updated_task.due_date,
        category=updated_task.category,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )
