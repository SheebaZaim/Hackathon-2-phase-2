from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class SchoolPlanningBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    subject: str
    grade_level: str
    date: datetime
    duration: Optional[int] = None
    materials_needed: Optional[str] = None
    learning_objectives: Optional[str] = None
    class_size: Optional[int] = None
    teaching_method: Optional[str] = None
    assessment_type: Optional[str] = None
    standards_addressed: Optional[str] = None
    previous_knowledge_required: Optional[str] = None
    extension_activities: Optional[str] = None
    differentiation_strategies: Optional[str] = None
    resources_links: Optional[str] = None

class SchoolPlanning(SchoolPlanningBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SchoolPlanningCreate(SchoolPlanningBase):
    pass

class SchoolPlanningUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[str] = None
    date: Optional[datetime] = None
    duration: Optional[int] = None
    materials_needed: Optional[str] = None
    learning_objectives: Optional[str] = None
    class_size: Optional[int] = None
    teaching_method: Optional[str] = None
    assessment_type: Optional[str] = None
    standards_addressed: Optional[str] = None
    previous_knowledge_required: Optional[str] = None
    extension_activities: Optional[str] = None
    differentiation_strategies: Optional[str] = None
    resources_links: Optional[str] = None

class SchoolPlanningResponse(SchoolPlanningBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime