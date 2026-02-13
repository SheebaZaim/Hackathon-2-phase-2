"""TodoList model for organizing tasks into lists"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class TodoList(SQLModel, table=True):
    """TodoList model for organizing tasks"""

    __tablename__ = "todo_lists"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(default=None, max_length=500)
    color: Optional[str] = Field(default="#3B82F6", max_length=20)  # Default blue
    icon: Optional[str] = Field(default="📝", max_length=10)
    is_default: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Work Tasks",
                "description": "Tasks related to work projects",
                "color": "#3B82F6",
                "icon": "💼",
                "is_default": True,
                "created_at": "2026-02-12T12:00:00Z",
                "updated_at": "2026-02-12T12:00:00Z"
            }
        }


class TodoListCreate(SQLModel):
    """Request model for creating a todo list"""

    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    color: Optional[str] = Field(default="#3B82F6", max_length=20)
    icon: Optional[str] = Field(default="📝", max_length=10)
    is_default: Optional[bool] = Field(default=False)


class TodoListUpdate(SQLModel):
    """Request model for updating a todo list"""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    color: Optional[str] = Field(default=None, max_length=20)
    icon: Optional[str] = Field(default=None, max_length=10)
    is_default: Optional[bool] = None


class TodoListResponse(SQLModel):
    """Response model for todo list"""

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    is_default: bool
    task_count: Optional[int] = 0  # Number of tasks in this list
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Work Tasks",
                "description": "Tasks related to work projects",
                "color": "#3B82F6",
                "icon": "💼",
                "is_default": True,
                "task_count": 5,
                "created_at": "2026-02-12T12:00:00Z",
                "updated_at": "2026-02-12T12:00:00Z"
            }
        }
