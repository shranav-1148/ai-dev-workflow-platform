from fastapi import APIRouter, Depends
from app.schemas.repositories import RepositoryCreate, RepositoryResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.repositories import Repository


router = APIRouter(prefix="/repositories")

@router.get("/", response_model=list[RepositoryResponse])
def get_repositories(db : Session = Depends(get_db)):
    repositories = db.query(Repository).all()

    return repositories

@router.get("/{repo_id}", response_model=RepositoryResponse)
def get_repository(repo_id: int, db : Session = Depends(get_db)):
    repository = db.query(Repository).filter(Repository.id == repo_id).first()
    
    return repository


@router.post("/", response_model=RepositoryResponse)
def create_repository(repo: RepositoryCreate, db:Session = Depends(get_db)):
    db_repo = Repository(
        name=repo.name,
        github_url=repo.github_url
    )

    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)

    return db_repo



    