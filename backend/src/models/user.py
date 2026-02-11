"""User model for Todo App - SQLModel definition per data-model.md"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class User(SQLModel, table=True):
    """User model for authentication and task ownership"""

    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    first_name: Optional[str] = Field(default="", max_length=100)
    last_name: Optional[str] = Field(default="", max_length=100)
    password_hash: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password_hash": "$2b$12$...",
                "created_at": "2026-02-09T12:00:00Z",
                "updated_at": "2026-02-09T12:00:00Z"
            }
        }


class UserResponse(SQLModel):
    """User response model (without password_hash)"""

    id: uuid.UUID
    email: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-02-09T12:00:00Z"
            }
        }
