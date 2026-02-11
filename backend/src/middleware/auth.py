"""JWT authentication middleware for Todo App - per research.md"""
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os
from sqlmodel import Session, select
from uuid import UUID

from ..models.user import User, UserResponse
from ..database.connection import get_session

# Get secret from environment - MUST match frontend BETTER_AUTH_SECRET
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")

ALGORITHM = "HS256"

security = HTTPBearer()


def verify_token(token: str) -> dict:
    """Verify a JWT token and return the payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> dict:
    """
    Get the current user from the JWT token.
    Returns dict with user_id for use in API endpoints.
    """
    token = credentials.credentials
    payload = verify_token(token)

    # Extract user_id from token payload (user_id claim)
    user_id_str: str = payload.get("user_id")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token"
        )

    # Optional: Verify user still exists in database
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement)
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Return user context for use in endpoints
    return {
        "user_id": user.id,
        "email": user.email
    }
