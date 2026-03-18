from pydantic import BaseModel


class FixPlan(BaseModel):
    id: str
    incident_id: str
    action: str
    explanation: str
    root_cause: str = ""
    parameters: dict = {}