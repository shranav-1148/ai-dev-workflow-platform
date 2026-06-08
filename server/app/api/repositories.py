from fastapi import APIRouter, Depends, HTTPException
from app.schemas.repositories import RepositoryCreate, RepositoryResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.repositories import Repository
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/repositories")

@router.get("/", response_model=list[RepositoryResponse])
def get_repositories(
        db : Session = Depends(get_db),
        current_user: User = Depends(get_current_user)

    ):
    '''Get all repositories of current user'''

    return db.query(Repository).filter(
        Repository.user_id == current_user.id
    ).all()

@router.get("/{repo_id}", response_model=RepositoryResponse)
def get_repository(
        repo_id: int,
        db : Session = Depends(get_db),
        current_user: User = Depends(get_current_user)    
    ):

    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.user_id == current_user.id
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Not Found")
    
    return repo


@router.post("/", response_model=RepositoryResponse)
def create_repository(
        repo: RepositoryCreate, 
        db:Session = Depends(get_db), 
        current_user: User= Depends(get_current_user)
    ):

    db_repo = Repository(
        name=repo.name,
        github_url=repo.github_url,
        user_id = current_user.id
    )

    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)

    return db_repo



    