from pydantic import BaseModel


class FixPlan(BaseModel):
    id: str
    incident_id: str
    action: str
    explanation: str
    parameters: dict = {}