from fastapi import APIRouter
from app.schemas.repositories import RepositoryCreate, RepositoryResponse


router = APIRouter(prefix="/repositories")

@router.get("/")
def get_repositories():
    return [
        RepositoryResponse(id=1, name="repo-1", url="https://example.com/repo-1"),
        RepositoryResponse(id=2, name="repo-2", url="https://example.com/repo-2"),
    ]

@router.get("/{repo_id}")
def get_repository(repo_id: int):
    return RepositoryResponse(id=repo_id, name=f"repo-{repo_id}", url=f"https://example.com/repo-{repo_id}")


@router.post("/", response_model=RepositoryResponse)
def create_repository(repo: RepositoryCreate):

    return RepositoryResponse(
        id = 1,
        name=repo.name,
        github_url=repo.github_url
    )