from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.todo_list import TodoList


class TaskService:
    """Service class for task-related operations."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieve a task by its ID."""
        statement = select(Task).where(Task.id == task_id)
        return self.db_session.exec(statement).first()
    
    def get_tasks_by_todo_list(self, todo_list_id: UUID) -> List[Task]:
        """Retrieve all tasks for a specific todo list."""
        statement = select(Task).where(Task.todo_list_id == todo_list_id)
        return self.db_session.exec(statement).all()
    
    def create_task(self, task_create: TaskCreate, todo_list_id: UUID) -> Task:
        """Create a new task in a specific todo list."""
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            is_completed=task_create.is_completed,
            priority=task_create.priority,
            due_date=task_create.due_date,
            todo_list_id=todo_list_id,
            position=task_create.position
        )
        
        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)
        
        return db_task
    
    def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Update an existing task."""
        db_task = self.get_task_by_id(task_id)
        if not db_task:
            return None
        
        # Update fields if they are provided
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.is_completed is not None:
            db_task.is_completed = task_update.is_completed
            # If task is being marked as completed, set completed_at timestamp
            if task_update.is_completed and not db_task.completed_at:
                db_task.completed_at = datetime.utcnow()
            # If task is being marked as incomplete, clear completed_at timestamp
            elif not task_update.is_completed:
                db_task.completed_at = None
        if task_update.priority is not None:
            db_task.priority = task_update.priority
        if task_update.due_date is not None:
            db_task.due_date = task_update.due_date
        if task_update.position is not None:
            db_task.position = task_update.position
        
        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)
        
        return db_task
    
    def delete_task(self, task_id: UUID) -> bool:
        """Delete a task."""
        db_task = self.get_task_by_id(task_id)
        if not db_task:
            return False
        
        self.db_session.delete(db_task)
        self.db_session.commit()
        return True
    
    def toggle_task_completion(self, task_id: UUID) -> Optional[Task]:
        """Toggle the completion status of a task."""
        db_task = self.get_task_by_id(task_id)
        if not db_task:
            return None
        
        # Toggle completion status
        db_task.is_completed = not db_task.is_completed
        
        # Set completed_at timestamp if task is being marked as completed
        if db_task.is_completed and not db_task.completed_at:
            db_task.completed_at = datetime.utcnow()
        # Clear completed_at timestamp if task is being marked as incomplete
        elif not db_task.is_completed:
            db_task.completed_at = None
        
        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)
        
        return db_task
    
    def check_todo_list_owns_task(self, todo_list_id: UUID, task_id: UUID) -> bool:
        """Check if a todo list owns a specific task."""
        statement = select(Task).where(
            Task.id == task_id,
            Task.todo_list_id == todo_list_id
        )
        task = self.db_session.exec(statement).first()
        return task is not None