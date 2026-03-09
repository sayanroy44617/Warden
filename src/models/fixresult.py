from pydantic import BaseModel


class FixResult(BaseModel):
    id: str
    incident_id: str
    success: bool
    isHealthy: bool
    message: str = ""