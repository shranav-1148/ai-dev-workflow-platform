from pydantic import BaseModel, EmailStr

# UserCreate is used internally for creating a new user used for admins, seeding and testing
class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    github_id: int
    created_at: str

# Schema used when user registers from frontend
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email : str

    model_config = {
        "from_attributes": True
    }

