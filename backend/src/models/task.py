from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=200)
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)
    todo_list_id: uuid.UUID = Field(foreign_key="todolist.id", nullable=False)
    position: int = Field(default=0)


class Task(TaskBase, table=True):
    """Task model for the application."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
    position: Optional[int] = None


class TaskPublic(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None