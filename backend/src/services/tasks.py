"""Task service with CRUD operations and user isolation"""
from sqlmodel import Session, select
from uuid import UUID
from typing import List, Optional
from datetime import datetime

from ..models.task import Task, TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    """Service for task CRUD operations with user isolation"""

    @staticmethod
    def create_task(
        session: Session,
        user_id: UUID,
        task_data: TaskCreate
    ) -> Task:
        """Create a new task for a user"""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_tasks(
        session: Session,
        user_id: UUID,
        completed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Task]:
        """Get all tasks for a user with optional filtering"""
        statement = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            statement = statement.where(Task.completed == completed)

        statement = statement.offset(offset).limit(limit)
        result = session.exec(statement)
        return result.all()

    @staticmethod
    def get_task(
        session: Session,
        user_id: UUID,
        task_id: UUID
    ) -> Optional[Task]:
        """Get a specific task (with user isolation)"""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Ensure user owns this task
        )
        result = session.exec(statement)
        return result.first()

    @staticmethod
    def update_task(
        session: Session,
        user_id: UUID,
        task_id: UUID,
        task_data: TaskUpdate
    ) -> Optional[Task]:
        """Update a task (with user isolation)"""
        task = TaskService.get_task(session, user_id, task_id)

        if not task:
            return None

        # Update only provided fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed

        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(
        session: Session,
        user_id: UUID,
        task_id: UUID
    ) -> bool:
        """Delete a task (with user isolation)"""
        task = TaskService.get_task(session, user_id, task_id)

        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def count_tasks(
        session: Session,
        user_id: UUID,
        completed: Optional[bool] = None
    ) -> int:
        """Count total tasks for a user"""
        statement = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            statement = statement.where(Task.completed == completed)

        result = session.exec(statement)
        return len(result.all())
