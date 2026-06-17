from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.github_service import GithubService
from app.models.repositories import Repository
from app.schemas.importRepoRequest import ImportRepositoryRequest

router = APIRouter(prefix="/github")


@router.get("/repos")
def get_github_repos(
    current_user: User  = Depends(get_current_user)
):
    if not current_user.github_access_token:
        raise HTTPException(
            status_code=400,
            detail="Github account not connected"
        )
    
    github_service = GithubService(
        current_user.github_access_token
    )

    repos = github_service.get_user_repos()

    return repos


@router.post("/repos/import")
def import_repos(
    repo: ImportRepositoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.github_access_token:
        raise HTTPException(
            status_code=400,
            detail="Github account not connected"
        )
    
    github_service = GithubService(
        current_user.github_access_token
    )

    github_repo = github_service.get_repo_by_id(
        repo.github_repo_id
    )

    existing_repo = (
        db.query(Repository)
        .filter(
            Repository.github_repo_id == github_repo["id"],
            Repository.user_id == current_user.id
        )
        .first()
    )

    if existing_repo:
        raise HTTPException(
            status_code=400,
            details="Repository already imported"
        )
    
    repository = Repository(
        github_repo_id=github_repo["id"],
        name=github_repo["name"],
        full_name=github_repo["full_name"],
        github_url=github_repo["html_url"],
        clone_url=github_repo["clone_url"],
        default_branch=github_repo["default_branch"],
        private=github_repo["private"],
        description=github_repo["description"],
        user_id=current_user.id
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository