# Simplified update status representation for the service
# Using a regular class instead of Pydantic model to avoid compatibility issues

from datetime import datetime
from enum import Enum
from typing import List, Optional


class UpdateStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class UpdateStatusModel:
    """
    Model for tracking the status of an update operation
    """
    def __init__(self,
                 update_id: str,
                 component_name: str,
                 status: UpdateStatusEnum,
                 started_at: datetime = None,
                 completed_at: datetime = None,
                 changes_applied: List[str] = None,
                 errors: List[str] = None,
                 warnings: List[str] = None,
                 rollback_possible: bool = True,
                 rollback_steps: List[str] = None,
                 recommendation_description: str = "",
                 estimated_duration_hours: float = None,
                 actual_duration_hours: float = None):
        self.update_id = update_id
        self.component_name = component_name
        self.status = status
        self.started_at = started_at
        self.completed_at = completed_at
        self.changes_applied = changes_applied or []
        self.errors = errors or []
        self.warnings = warnings or []
        self.rollback_possible = rollback_possible
        self.rollback_steps = rollback_steps or []
        self.recommendation_description = recommendation_description
        self.estimated_duration_hours = estimated_duration_hours
        self.actual_duration_hours = actual_duration_hours
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()