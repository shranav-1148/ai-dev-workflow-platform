from pydantic import BaseModel, ConfigDict
from datetime import datetime

class WorkflowStepCreate(BaseModel):
    name: str
    step_type: str
    config: dict
    order: int
    condition: str | None = None

class WorkflowStepUpdate(BaseModel):
    name: str | None = None
    step_type: str | None = None
    config: dict | None = None
    order: int | None = None
    condition: str | None = None

class WorkflowStepResponse(BaseModel):
    id: int
    workflow_id: int

    name: str
    step_type: str
    config: dict
    order: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes = True
    )

    condition: str | None = None