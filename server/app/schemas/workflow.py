from pydantic import BaseModel, ConfigDict
from datetime import datetime

class WorkflowCreate(BaseModel):
    name: str
    description: str
    

class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str | None

    respository_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkflowUpdate(BaseModel):
    name:str| None = None
    description: str | None = None