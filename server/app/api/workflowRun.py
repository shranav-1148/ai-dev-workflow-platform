from fastapi import APIRouter, Depends, HTTPException
from app.schemas.workflowRun import WorkflowRunResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.workflowRun import WorkflowRun
from app.core.security import get_current_user
from app.models.user import User
from app.models.repositories import Repository
from app.models.workflow import Workflow

'''
POST /workflows/{workflow_id}/run

GET /workflows/{workflow_id}/runs

GET /runs/{run_id}
'''

router = APIRouter(prefix="")

@router.post("/workflows/{workflow_id}/run", response_model = WorkflowRunResponse)
def create_run(
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
        ).first()
    )

    run = WorkflowRun(
        workflow_id = workflow_id,
        status="Running"
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    return run


@router.get("/workflows/{workflow_id}/runs", response_model = list[WorkflowRunResponse])
def get_runs(
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
        ).first()
    )

    if not workflow:
        raise HTTPException(
            status_code = 404,
            detail = "Workflow not found"
        )

    runs = (
        db.query(WorkflowRun)
        .filter(
            WorkflowRun.workflow_id== workflow_id
        ).all()
    )

    return runs
    

@router.get("/runs/{run_id}", response_model = WorkflowRunResponse)
def get_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    run = (
        db.query(WorkflowRun)
        .join(Workflow)
        .join(Repository)
        .filter(
            WorkflowRun.id == run_id,
            Repository.user_id == current_user.id
        ).fiirst()
    )

    if not run:
        raise HTTPException(
            status_code = 404,
            detail = "Run not found"
        )

    return run