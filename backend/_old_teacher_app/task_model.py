from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    due_date: datetime
    category: str
    priority: str = Field(default="medium")  # low, medium, high
    assigned_class: Optional[str] = None
    subject_area: Optional[str] = None
    estimated_time: Optional[int] = None  # in minutes
    related_planning_id: Optional[uuid.UUID] = Field(default=None, foreign_key="schoolplanning.id")
    students_involved: Optional[str] = None  # comma-separated list
    recurring: bool = Field(default=False)
    recurring_frequency: Optional[str] = None  # daily, weekly, monthly
    reminders_enabled: bool = Field(default=False)
    remind_before: Optional[int] = Field(default=None)  # minutes before due date

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = None
    actual_time: Optional[int] = None  # actual time taken in minutes
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    category: Optional[str] = None
    priority: Optional[str] = None  # low, medium, high
    completed: Optional[bool] = None
    assigned_class: Optional[str] = None
    subject_area: Optional[str] = None
    estimated_time: Optional[int] = None  # in minutes
    related_planning_id: Optional[uuid.UUID] = Field(default=None, foreign_key="schoolplanning.id")
    students_involved: Optional[str] = None  # comma-separated list
    recurring: Optional[bool] = None
    recurring_frequency: Optional[str] = None  # daily, weekly, monthly
    reminders_enabled: Optional[bool] = None
    remind_before: Optional[int] = None  # minutes before due date

class TaskResponse(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    completed: bool
    completed_at: Optional[datetime] = None
    actual_time: Optional[int] = None  # actual time taken in minutes
    created_at: datetime
    updated_at: datetime