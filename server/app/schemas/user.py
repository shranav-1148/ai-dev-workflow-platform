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

# Schema used when user logs in from frontend
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# The response model for user details
class UserResponse(BaseModel):
    id: int
    username: str
    email : str

    model_config = {
        "from_attributes": True
    }

# The response model for the JWT token after successful login
class Token(BaseModel):
    access_token : str
    token_type: str