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
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: bool = Field(default=False, nullable=False)
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


class TaskUpdate(SQLModel):
    """Request model for updating a task"""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: Optional[bool] = None


class TaskResponse(SQLModel):
    """Response model for task"""

    id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
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
