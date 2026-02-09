from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskTemplate(BaseModel):
    """
    Template for creating implementation tasks
    """
    id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus = TaskStatus.TODO
    assignee: str = Field(default=None)
    created_at: datetime
    updated_at: datetime
    due_date: datetime = Field(default=None)
    estimated_effort_hours: int = Field(default=None)  # Estimated time in hours
    dependencies: List[str] = Field(default_factory=list)  # List of task IDs this task depends on
    tags: List[str] = Field(default_factory=list)  # Tags for categorization
    acceptance_criteria: List[str] = Field(default_factory=list)  # List of acceptance criteria
    implementation_notes: str = Field(default=None)  # Additional implementation details
    related_user_story: str = Field(default=None)  # Link to user story if applicable
    files_affected: List[str] = Field(default_factory=list)  # List of files this task affects
    test_scenarios: List[str] = Field(default_factory=list)  # Test scenarios to verify completion