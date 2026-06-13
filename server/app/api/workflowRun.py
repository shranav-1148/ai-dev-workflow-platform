from fastapi import APIRouter, Depends, HTTPException
from app.schemas.workflowRun import WorkflowRunResponse
from app.schemas.workflowStepRun import WorkflowStepRunResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.workflowRun import WorkflowRun
from app.models.workflowStep import WorkflowStep
from app.models.workflowStepRun import WorkflowStepRun
from app.core.security import get_current_user
from app.models.user import User
from app.models.repositories import Repository
from app.models.workflow import Workflow
from app.services.workflow_executor import execute_workflow

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
    '''Create a new workflow run, effectively running a workflow'''
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
            detail="Workflow not found"
        )

    
    return execute_workflow(
        workflow,
        db
    )


@router.get("/workflows/{workflow_id}/runs", response_model = list[WorkflowRunResponse])
def get_runs(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''
        Get all runs of the specified workflow
    '''
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
    '''
        Get a specified run information
    '''
    run = (
        db.query(WorkflowRun)
        .join(Workflow)
        .join(Repository)
        .filter(
            WorkflowRun.id == run_id,
            Repository.user_id == current_user.id
        ).first()
    )

    if not run:
        raise HTTPException(
            status_code = 404,
            detail = "Run not found"
        )

    return run


@router.get("/runs/{run_id}/steps", response_model = list[WorkflowStepRunResponse])
def get_steps_from_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Return everything that happened during workflow run step-by-step'''
    run = (
        db.query(WorkflowRun)
        .join(Workflow)
        .join(Repository)
        .filter(
            WorkflowRun.id == run_id,
            Repository.user_id == current_user.id
        ).first()
    )

    if not run:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )
    
    step_runs = (
        db.query(WorkflowStepRun)
        .filter(
            WorkflowStepRun.workflow_run_id == run_id
        ).all()
    )

    return step_runs


@router.get("/runs/{run_id}/steps/{step_run_id}", response_model = WorkflowStepRunResponse)
def get_one_step_from_run(
    run_id: int,
    step_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Shoe detailed information for one step execution'''

    step_run = (
        db.query(WorkflowStepRun)
        .join(WorkflowRun)
        .join(Workflow)
        .join(Repository)
        .filter(
            WorkflowStepRun.id == step_run_id,
            WorkflowRun.id == run_id,
            Repository.user_id == current_user.id
        ).first()
    )

    if not step_run:
        raise HTTPException(
            status_code=404,
            detail="Step run not found"
        )
    
    return step_run