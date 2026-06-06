from http.client import HTTPException

from fastapi import APIRouter
from server.app.schemas.user import UserResponse, UserRegister
from server.app.db.database import get_db
from sqlalchemy.orm import Session, Depends
from server.app.models.user import User

from app.core.security import hash_password

router = APIRouter()

@router.post("/auth/register", response_model= UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    
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



