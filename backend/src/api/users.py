"""User profile API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from typing import Optional

from ..models.user import User
from ..middleware.auth import get_current_user
from ..database.connection import get_session

router = APIRouter(prefix="/users", tags=["users"])


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: str


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get current authenticated user's profile"""
    user_id = auth_data["user_id"]

    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at.isoformat()
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    update_data: UserUpdateRequest,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update current authenticated user's profile"""
    user_id = auth_data["user_id"]

    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields if provided
    if update_data.first_name is not None:
        user.first_name = update_data.first_name
    if update_data.last_name is not None:
        user.last_name = update_data.last_name
    if update_data.email is not None:
        # Check if email is already taken
        existing = session.exec(
            select(User).where(User.email == update_data.email, User.id != user_id)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        user.email = update_data.email

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at.isoformat()
    )
