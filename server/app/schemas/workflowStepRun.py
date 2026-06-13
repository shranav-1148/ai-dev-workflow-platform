from datetime import datetime
from pydantic import BaseModel, ConfigDict

class WorkflowStepRunResponse(BaseModel):
    id: int

    workflow_run_id: int

    workflow_step_id: int

    status: str

    output: dict | None = None

    error_message: str | None = None

    started_at: datetime

    completed_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )   