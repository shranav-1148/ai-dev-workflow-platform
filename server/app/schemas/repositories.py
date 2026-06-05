from pydantic import BaseModel

class RepositoryCreate(BaseModel):
    name: str
    github_url : str

class RepositoryResponse(BaseModel):
    id: int
    name: str
    github_url : str

