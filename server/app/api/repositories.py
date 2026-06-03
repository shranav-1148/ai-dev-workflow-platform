from fastapi import APIRouter

router = APIRouter(prefix="/repositories")

@router.get("/")
def get_repositories():
    return [
        {"id": 1, "name": "repo-a"},
        {"id": 2, "name": "repo-b"}
    ]