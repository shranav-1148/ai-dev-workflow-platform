from pydantic import BaseModel

class ImportRepositoryRequest(BaseModel):
    github_repo_id: int
    name: str
    full_name: str
    private: bool