from fastapi import APIRouter, Depends, HTTPException
from app.schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowUpdate
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.workflow import Workflow
from app.core.security import get_current_user
from app.models.user import User
from app.models.repositories import Repository

router = APIRouter(prefix="")


@router.post("/repositories/{repo_id}/workflows", response_model=WorkflowResponse)
def create_workflow(
    repo_id: int,
    workflow: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Creates a workflow for a specified repository'''
    repository = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.user_id == current_user.id
    ).first()

    if not repository:
        raise HTTPException(status_code = 404, detail="Repository not found")
    
    db_workflow = Workflow(
        name = workflow.name,
        description = workflow.description,
        repository_id = repo_id
    )

    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)

    return db_workflow


@router.get("/repositories/{repo_id}/workflows", response_model = WorkflowResponse)
def get_workflows(
    repo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Returns all the workflows of a given repository'''
    repository = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.user_id == current_user.id
    )

    if not repository:
        raise HTTPException(status_code = 404, detail="Repository not found")
    
    db_workflows = db.query(Workflow).filter(
        Workflow.repository_id == repo_id
    ).all()

    return db_workflows

@router.get("/workflows/{workflow_id}", response_model = WorkflowResponse)
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Returns a specific workflow'''
    
    workflow = db.query(Workflow).join(Repository).filter(
        Workflow.id == workflow_id,
        Repository.user_id == current_user.id
    ).first()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return workflow


@router.patch("/workflows/{workflow_id}", response_model = WorkflowResponse)
def update_workflow(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ''' Updates a specific workflow'''
    workflow = (
        db.query(Workflow).join(Repository).filter(
            Workflow.id == workflow_id,
            Repository.user_id == current_user.id
        ).first()
    )

    if not workflow:
        raise HTTPException(status_code = 404, detail = "Workflow not found")
    
    update_data = workflow_update.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(workflow, field, value)

    db.commit()
    db.refresh(workflow)

    return workflow

@router.delete("/workflows/{workflow_id}", status_code = 204)
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Deletes the specified workflow'''
    workflow = (
        db.query(Workflow).join(Repository).filter(
            Workflow.id == workflow_id,
            Repository.user_id == current_user.id
        ).first()
    )

    if not workflow:
        raise HTTPException(status_code = 404, detail = "Workflow not found")

    db.delete(workflow)
    db.commit()
