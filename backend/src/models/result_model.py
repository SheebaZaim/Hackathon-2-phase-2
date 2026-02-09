from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class ResultBase(SQLModel):
    student_id: uuid.UUID = Field(foreign_key="student.id")
    subject_id: uuid.UUID = Field(foreign_key="subject.id")
    score: float  # Numeric score (e.g., percentage)
    grade: str    # Letter grade (e.g., A+, B-, etc.)
    assignment_name: str
    assignment_date: datetime = Field(default_factory=datetime.utcnow)

class Result(ResultBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student_: "Student" = Relationship(back_populates="results")
    subject: "Subject" = Relationship(back_populates="results")

class ResultCreate(ResultBase):
    pass

class ResultUpdate(SQLModel):
    score: Optional[float] = None
    grade: Optional[str] = None
    assignment_name: Optional[str] = None
    assignment_date: Optional[datetime] = None

class ResultResponse(SQLModel):
    id: uuid.UUID
    student_id: uuid.UUID
    subject_id: uuid.UUID
    score: float
    grade: str
    assignment_name: str
    assignment_date: datetime
    created_at: datetime
    updated_at: datetime