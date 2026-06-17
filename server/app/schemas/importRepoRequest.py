from pydantic import BaseModel

class ImportRepositoryRequest(BaseModel):
    github_repo_id: int
    