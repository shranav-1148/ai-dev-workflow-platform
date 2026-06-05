from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    github_id: int
    created_at: str

class UserResponse(BaseModel):
    id: int
    username: str
    email : str

