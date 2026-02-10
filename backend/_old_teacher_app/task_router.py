from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, update
from typing import List
from uuid import UUID
from datetime import datetime

from ..db import get_session
from ..models.task_model import Task, TaskCreate, TaskUpdate, TaskResponse
from ..middleware.jwt_middleware import get_current_user
from ..models.user_model import UserResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    # Create new task with the current user's ID
    task = Task(
        **task_data.dict(),
        user_id=current_user.id
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        category=task.category,
        priority=task.priority,
        completed=task.completed,
        completed_at=task.completed_at,
        assigned_class=task.assigned_class,
        subject_area=task.subject_area,
        estimated_time=task.estimated_time,
        actual_time=task.actual_time,
        related_planning_id=task.related_planning_id,
        students_involved=task.students_involved,
        recurring=task.recurring,
        recurring_frequency=task.recurring_frequency,
        reminders_enabled=task.reminders_enabled,
        remind_before=task.remind_before,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user"""
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    
    task_list = []
    for task in tasks:
        task_list.append(TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            category=task.category,
            priority=task.priority,
            completed=task.completed,
            completed_at=task.completed_at,
            assigned_class=task.assigned_class,
            subject_area=task.subject_area,
            estimated_time=task.estimated_time,
            actual_time=task.actual_time,
            related_planning_id=task.related_planning_id,
            students_involved=task.students_involved,
            recurring=task.recurring,
            recurring_frequency=task.recurring_frequency,
            reminders_enabled=task.reminders_enabled,
            remind_before=task.remind_before,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        ))
    return task_list


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for the current user"""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        category=task.category,
        priority=task.priority,
        completed=task.completed,
        completed_at=task.completed_at,
        assigned_class=task.assigned_class,
        subject_area=task.subject_area,
        estimated_time=task.estimated_time,
        actual_time=task.actual_time,
        related_planning_id=task.related_planning_id,
        students_involved=task.students_involved,
        recurring=task.recurring,
        recurring_frequency=task.recurring_frequency,
        reminders_enabled=task.reminders_enabled,
        remind_before=task.remind_before,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task for the current user"""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update the task with the new data
    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(task, field, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        category=task.category,
        priority=task.priority,
        completed=task.completed,
        completed_at=task.completed_at,
        assigned_class=task.assigned_class,
        subject_area=task.subject_area,
        estimated_time=task.estimated_time,
        actual_time=task.actual_time,
        related_planning_id=task.related_planning_id,
        students_involved=task.students_involved,
        recurring=task.recurring,
        recurring_frequency=task.recurring_frequency,
        reminders_enabled=task.reminders_enabled,
        remind_before=task.remind_before,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_completion(
    task_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task for the current user"""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Toggle completion status
    task.completed = not task.completed
    if task.completed:
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        category=task.category,
        priority=task.priority,
        completed=task.completed,
        completed_at=task.completed_at,
        assigned_class=task.assigned_class,
        subject_area=task.subject_area,
        estimated_time=task.estimated_time,
        actual_time=task.actual_time,
        related_planning_id=task.related_planning_id,
        students_involved=task.students_involved,
        recurring=task.recurring,
        recurring_frequency=task.recurring_frequency,
        reminders_enabled=task.reminders_enabled,
        remind_before=task.remind_before,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task for the current user"""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    session.delete(task)
    session.commit()
    
    return {"message": "Task deleted successfully"}