from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User


router = APIRouter(prefix="/users")

@router.get("/", response_model=list[UserResponse])
def get_users(db : Session = Depends(get_db)):
    users = db.query(User).all()

    return users

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    return user


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db:Session = Depends(get_db)):
    db_repo = User(
        name=user.name,
        email=user.email
    )

    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)

    return db_repo



    