from pydantic import BaseModel, ConfigDict
from datetime import datetime

class WorkflowRunResponse(BaseModel):
    id: int
    workflow_id: int
    status: str
    started_at: datetime

    completed_at: datetime | None

    model_config= ConfigDict(
        from_attributes = True
    )
