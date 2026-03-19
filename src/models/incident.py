from enum import Enum
from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class IncidentStatusEnum(Enum):
    DETECTED = "detected"
    RESOLVED = "resolved"
    ANALYZING = "analyzing"
    PENDING_APPROVAL = "pending_approval"
    EXECUTING = "executing"
    FAILED = "failed"


class SeverityEnum(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Incident(BaseModel):
    id: str
    timestamp: datetime
    container_name: str
    logs: list[str]
    crash_reason: Optional[str]
    severity: SeverityEnum
    incident_status: IncidentStatusEnum = IncidentStatusEnum.DETECTED
