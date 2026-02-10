from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from .class_model import Class

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    classes: List[Class] = Relationship(back_populates="teacher")

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(SQLModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime