from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class SubjectBase(SQLModel):
    name: str = Field(unique=True, index=True)  # e.g., "Mathematics", "Science"
    code: str = Field(unique=True, index=True)  # e.g., "MATH101", "SCI201"
    description: Optional[str] = None

class Subject(SubjectBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    results: List["Result"] = Relationship(back_populates="subject_")

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SQLModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

class SubjectResponse(SQLModel):
    id: uuid.UUID
    name: str
    code: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime