from enum import Enum

from pydantic import BaseModel

class FixActionEnum(str, Enum):
    RESTART = "restart"
    UPDATE_RESOURCES = "update_resources"
    EXEC_COMMAND = "exec_command"

class FixPlan(BaseModel):
    id: str
    incident_id: str
    container_name: str
    action: FixActionEnum
    explanation: str
    root_cause: str = ""
    parameters: dict = {}
