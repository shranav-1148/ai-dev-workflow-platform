from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.github_service import GithubService

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