from http.client import HTTPException

from fastapi import APIRouter
from server.app.schemas.user import UserResponse, UserRegister, userLogin, Token
from server.app.db.database import get_db
from sqlalchemy.orm import Session, Depends
from server.app.models.user import User

from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/auth/register", response_model= UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    '''
        Registers a new user and returns the user details'''
    
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    db_user = User(
        username = user.username,
        email = user.email,
        password = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("auth/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    '''
        Authenticates the user and returns a JWT token if successful
    '''
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(
        data={"sub": str(db_user.id)}
    )

    finalToken = Token(
        access_token = token,
        token_type = "bearer"

    )

    return finalToken


