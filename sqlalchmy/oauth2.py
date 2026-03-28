# 8 
# Import JWT functions for encoding and decoding tokens
# any time user want to logged in we can adde xtra dependency to path operation on any router any time we need a fun that require logged it
# will create a token and will verify token an if there is no error return nothing and proper authentication 
from jose import jwt, JWTError

# Used to set token expiry time
from datetime import datetime, timedelta

# FastAPI utilities for dependency injection and error handling
from fastapi import Depends, HTTPException, status

# Your schema file (make sure spelling is correct: sqlalchemy.schemas or your module)
from . import schemas

# OAuth2PasswordBearer extracts token from request header
from fastapi.security import OAuth2PasswordBearer

from .config import settings


# This tells FastAPI:
# - The token will be sent in "Authorization: Bearer <token>"
# - tokenUrl="login" means client will get token from /login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Secret key used to sign JWT (keep it safe in real apps)
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# 🔹 Function to CREATE a JWT token
def create_access_token(data: dict):
    # Copy user data (like user_id)
    to_encode = data.copy()

    # Set expiry time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiry ("exp") to payload
    to_encode.update({
        "exp": expire  # expiry in UNIX timestamp
    })

    # Encode data into JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Return token
    return encoded_jwt


# 🔹 Function to VERIFY JWT token
def verify_access_token(token: str, credential_exception):
    try:
        print("TOKEN RECEIVED:", token)   # 🔥 ADD THIS

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("PAYLOAD:", payload)        # 🔥 ADD THIS

        id: str = payload.get("user_id")

        if not id:
            raise credential_exception

        return schemas.TokenData(id=id)

    except JWTError as e:
        print("JWT ERROR:", e)           # 🔥 ADD THIS
        raise credential_exception

# 🔹 Dependency function to get CURRENT USER
from . import model
from sqlalchemy.orm import Session
from .database import get_db

# once the verify access token get current get user from database 
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(model.User).filter(model.User.id == token_data.id).first()

    if user is None:
        raise credentials_exception

    return user