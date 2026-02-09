from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from sqlmodel import Session, select
from ..models.user_model import UserResponse
from ..db import get_session
from ..models.user_model import User

# Get secret from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_development")
ALGORITHM = "HS256"

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default 15 minutes
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify a JWT token and return the payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)) -> UserResponse:
    """Get the current user from the JWT token"""
    token = credentials.credentials
    payload = verify_token(token)

    user_id_str: str = payload.get("sub")
    email: str = payload.get("email")

    if user_id_str is None or email is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    try:
        from uuid import UUID
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID in token")

    # Fetch user details from the database
    statement = select(User).where(User.id == user_id, User.email == email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Create a proper user response object
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    return user_response