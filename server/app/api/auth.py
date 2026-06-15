
from fastapi import APIRouter, Depends, HTTPException
from  fastapi.responses import RedirectResponse
from app.core.config import settings
from app.schemas.user import UserResponse, UserRegister, UserLogin, Token
from app.core.security import get_current_user
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
import requests 
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/auth/register", response_model= UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    '''
        Registers a new user and returns the user details'''
    
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    print(user.password)
    print(len(user.password))
    hashed_password = hash_password(user.password)
    db_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/auth/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    '''
        Authenticates the user and returns a JWT token if successful
    '''
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(
        data={"user_id": str(db_user.id)}
    )

    finalToken = Token(
        access_token = token,
        token_type = "bearer"

    )

    return finalToken


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/auth/github")
def github_login():
    github_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        "&scope=repo"
    )

    return RedirectResponse(url=github_url)

@router.get("/auth/github/callback")
def github_callback(code: str):

    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers = {
            "Accept": "application/json"
        },
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code
        }
    )

    token_data =  response.json()

    access_token = token_data["access_token"]

    github_user = requests.get(
         "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json"
        }
    )

    return github_user.json()

    return response.json()


