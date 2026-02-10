from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class ClassBase(SQLModel):
    name: str
    subject: str
    grade_level: str

class Class(ClassBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    teacher_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    teacher: "User" = Relationship(back_populates="classes")
    students: List["Student"] = Relationship(back_populates="class_")

class ClassCreate(ClassBase):
    pass

class ClassUpdate(SQLModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[str] = None

class ClassResponse(SQLModel):
    id: uuid.UUID
    name: str
    subject: str
    grade_level: str
    teacher_id: uuid.UUID
    created_at: datetime
    updated_at: datetime