from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
import uuid

from ..db import get_session
from ..models.user_model import User, UserCreate, UserResponse, UserUpdate
from ..services.auth_service import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_user_response
)
from ..middleware.jwt_middleware import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# Request/response models
class UserRegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdateRequest(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class LogoutResponse(BaseModel):
    message: str = "Successfully logged out"


@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserRegisterRequest, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return create_user_response(user)


@router.post("/login", response_model=UserLoginResponse)
def login_user(user_data: UserLoginRequest, session: Session = Depends(get_session)):
    """Authenticate user and return access token"""
    # Find user by email
    statement = select(User).where(User.email == user_data.email)
    user = session.exec(statement).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # Token valid for 30 minutes
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return UserLoginResponse(access_token=access_token)


@router.post("/logout", response_model=LogoutResponse)
def logout_user():
    """Logout user (client-side token removal is sufficient for JWT)"""
    # For JWT tokens, the actual logout happens on the client side
    # where the token is removed from storage. This endpoint can be
    # used for additional cleanup if needed.
    return LogoutResponse(message="Successfully logged out")


@router.get("/profile", response_model=UserResponse)
def read_user_profile(current_user: UserResponse = Depends(get_current_user)):
    """Get the current user's profile information"""
    return current_user


@router.put("/profile", response_model=UserResponse)
def update_user_profile(
    user_update: UserUpdateRequest,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update the current user's profile information"""
    # Get the user from the database using the ID from the token
    statement = select(User).where(User.id == current_user.id)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields if provided
    if user_update.email is not None:
        # Check if email is already taken by another user
        existing_user = session.exec(
            select(User).where(User.email == user_update.email, User.id != current_user.id)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken by another user"
            )
        user.email = user_update.email
    
    if user_update.first_name is not None:
        user.first_name = user_update.first_name
        
    if user_update.last_name is not None:
        user.last_name = user_update.last_name
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return create_user_response(user)