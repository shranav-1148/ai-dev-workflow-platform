from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from dotenv import load_dotenv
from app.models.user import User
from app.db.database import get_db
from datetime import datetime, timedelta, timezone

import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")

def hash_password(user_password: str):
    ''' Hashes the user password using bcrypt and returns the hashed password'''
    return pwd_context.hash(user_password)

def verify_password(plain_password: str, hashed_password: str):
    ''' Verifies the plain password against the hashed password'''
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data: dict):
    ''' Creates a JWT access token with the given data and returns the token'''
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update(
        {"exp" : expire}
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
    

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code = 401, detail="Invalid token")
        
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)

    user_id: str = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code = 401, detail="Invalid token payload")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail="User not found")
    
    return user