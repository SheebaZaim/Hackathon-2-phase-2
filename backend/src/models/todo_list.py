from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class TodoListBase(SQLModel):
    title: str = Field(nullable=False, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    is_public: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    position: int = Field(default=0)


class TodoList(TodoListBase, table=True):
    """TodoList model for the application."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TodoListCreate(TodoListBase):
    pass


class TodoListUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    position: Optional[int] = None


class TodoListPublic(TodoListBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime