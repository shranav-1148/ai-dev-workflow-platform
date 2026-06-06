from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    

