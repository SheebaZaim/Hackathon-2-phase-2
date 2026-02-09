from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=100)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """User model for the application."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = Field(default=None)


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None


class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None