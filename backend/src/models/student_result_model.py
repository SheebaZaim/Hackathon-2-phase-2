from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class StudentResultBase(SQLModel):
    student_name: str
    assignment_title: str
    score: float
    max_score: float
    subject: str
    date_recorded: datetime
    comments: Optional[str] = None

class StudentResult(StudentResultBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    percentage: Optional[float] = Field(default=None)
    grade_letter: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StudentResultCreate(StudentResultBase):
    pass

class StudentResultUpdate(SQLModel):
    student_name: Optional[str] = None
    assignment_title: Optional[str] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    subject: Optional[str] = None
    date_recorded: Optional[datetime] = None
    comments: Optional[str] = None

class StudentResultResponse(StudentResultBase):
    id: uuid.UUID
    user_id: uuid.UUID
    percentage: Optional[float]
    grade_letter: Optional[str]
    created_at: datetime
    updated_at: datetime