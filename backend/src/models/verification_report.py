from enum import Enum
from typing import List
from pydantic import BaseModel


class StatusEnum(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    MISSING = "missing"
    WARNING = "warning"


class ComponentStatus(BaseModel):
    name: str
    status: StatusEnum
    details: str
    compliant: bool
    errors: List[str] = []
    warnings: List[str] = []


class VerificationReport(BaseModel):
    id: str
    timestamp: str
    version: str
    components_checked: List[ComponentStatus] = []
    total_components: int = 0
    passed_components: int = 0
    failed_components: int = 0
    missing_components: int = 0
    compliance_score: float = 0.0
    overall_status: str = "unknown"  # pass, fail, partial