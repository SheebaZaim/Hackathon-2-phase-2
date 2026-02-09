from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session
from ..models.user_model import UserResponse
from ..middleware.jwt_middleware import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/profile", response_model=UserResponse)
def read_user_profile(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get the current user's profile information"""
    return current_user