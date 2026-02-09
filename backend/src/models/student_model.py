from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class StudentBase(SQLModel):
    first_name: str
    last_name: str
    student_id: str = Field(unique=True, index=True)  # School-assigned ID

class Student(StudentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    class_id: uuid.UUID = Field(foreign_key="class.id")
    enrollment_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    class_: "Class" = Relationship(back_populates="students")
    results: List["Result"] = Relationship(back_populates="student_")

class StudentCreate(StudentBase):
    class_id: uuid.UUID

class StudentUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    class_id: Optional[uuid.UUID] = None

class StudentResponse(SQLModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    student_id: str
    class_id: uuid.UUID
    enrollment_date: datetime
    created_at: datetime
    updated_at: datetime