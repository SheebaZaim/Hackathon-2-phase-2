"""Task model for Todo App - SQLModel definition per data-model.md"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class Task(SQLModel, table=True):
    """Task model for todo items"""

    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)
    todo_list_id: Optional[uuid.UUID] = Field(default=None, foreign_key="todo_lists.id", index=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: bool = Field(default=False, nullable=False)
    priority: Optional[str] = Field(default="medium", max_length=20)
    due_date: Optional[datetime] = Field(default=None)
    category: Optional[str] = Field(default="", max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Complete project documentation",
                "description": "Write comprehensive docs for the API",
                "completed": False,
                "created_at": "2026-02-09T12:00:00Z",
                "updated_at": "2026-02-09T12:00:00Z"
            }
        }


class TaskCreate(SQLModel):
    """Request model for creating a task"""

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=10000)
    priority: Optional[str] = Field(default="medium", max_length=20)
    due_date: Optional[datetime] = Field(default=None)
    category: Optional[str] = Field(default="", max_length=100)
    todo_list_id: Optional[uuid.UUID] = Field(default=None)


class TaskUpdate(SQLModel):
    """Request model for updating a task"""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, max_length=20)
    due_date: Optional[datetime] = None
    category: Optional[str] = Field(default=None, max_length=100)
    todo_list_id: Optional[uuid.UUID] = None


class TaskResponse(SQLModel):
    """Response model for task"""

    id: uuid.UUID
    todo_list_id: Optional[uuid.UUID]
    title: str
    description: Optional[str]
    completed: bool
    priority: Optional[str]
    due_date: Optional[datetime]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "title": "Complete project documentation",
                "description": "Write comprehensive docs for the API",
                "completed": False,
                "created_at": "2026-02-09T12:00:00Z",
                "updated_at": "2026-02-09T12:00:00Z"
            }
        }
