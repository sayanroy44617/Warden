from pydantic import BaseModel


class FixResult(BaseModel):
    """
       Represents the result of a fix operation.

       Attributes:
           id: Unique identifier for the fix result
           incident_id: ID of the associated incident
           success: Whether the fix was successful
           is_healthy: Whether the system is healthy after the fix
           message: Optional message with additional details
    """
    id: str
    incident_id: str
    success: bool
    is_healthy: bool
    message: str = ""