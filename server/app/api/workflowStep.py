from fastapi import APIRouter, Depends, HTTPException
from app.schemas.workflowStep import WorkflowStepCreate, WorkflowStepResponse, WorkflowStepUpdate
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.workflowStep import WorkflowStep
from app.core.security import get_current_user
from app.models.user import User
from app.models.repositories import Repository
from app.models.workflow import Workflow

router = APIRouter(prefix="")

'''
POST   /workflows/{workflow_id}/steps
GET    /workflows/{workflow_id}/steps
PATCH  /steps/{step_id}
DELETE /steps/{step_id}
'''

@router.post("/workflows/{workflow_id}/steps", response_model = WorkflowStepResponse)
def create_workflowStep(
    workflow_id: int,
    workflow_step: WorkflowStepCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = (
        db.query(Workflow)
        .join(Repository)
        .filter(
            Workflow.id == workflow_id,
            Repository.user_id == current_user.id
        )
        .first()
    )

    if not workflow:
        raise HTTPException(
            status_code = 404,
            detail = "Workflow not found"
        )
    
    db_step = WorkflowStep(
        workflow_id = workflow_id,
        name = workflow_step.name,
        step_type = workflow_step.step_type,
        config = workflow_step.config,
        order = workflow_step.order
    )

    db.add(db_step)
    db.commit()
    db.refresh(db_step)

    return db_step

@router.get("/workflows/{workflow_id}/steps", response_model = list[WorkflowStepResponse])
def get_workflowStep(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = (
        db.query(Workflow)
        .join(Repository)
        .filter(
            Workflow.id == workflow_id,
            Repository.user_id == current_user.id
        )
        .first()
    )

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )
    
    workflow_steps = (
        db.query(WorkflowStep)
        .filter(
            WorkflowStep.workflow_id == workflow_id
        ).all()
    )

    return workflow_steps


@router.patch("/steps/{step_id}", response_model= WorkflowStepResponse)
def update_step(
    step_id: int,
    step_update: WorkflowStepUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    step = (
        db.query(WorkflowStep)
        .join(Workflow)
        .join(Repository)
        .filter(
            WorkflowStep.id == step_id,
            Repository.user_id == current_user.id
        )
        .first()
    )

    if not step:
        raise HTTPException(
            status_code=404,
            detail="Step not found"
        )
    
    update_data = step_update.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(step, field, value)


    db.commit()
    db.refresh(step)

    return step 

@router.delete("/steps/{step_id}", response_model = WorkflowStepResponse)
def delete_step(
    step_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    step = (
        db.query(WorkflowStep)
        .join(Workflow)
        .join(Repository)
        .filter(
            WorkflowStep.id == step_id,
            Repository.user_id == current_user.id
        )
        .first()
    )

    if not step:
        raise HTTPException(
            status_code=404,
            detail="Step not found"
        )
    db.delete(step)
    db.commit()

    return step

    
