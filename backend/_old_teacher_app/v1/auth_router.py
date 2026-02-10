from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import Optional
from ..database.session import get_db_session
from ..models.user import User, UserCreate, UserUpdate, UserPublic
from ..models.auth_token import AuthenticationToken
from ..services.user_service import UserService
from ..services.auth_service import AuthenticationService
from ..utils.responses import APIResponse, create_success_response
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserPublic)
async def register_user(user_create: UserCreate, db: Session = Depends(get_db_session)):
    """Register a new user."""
    user_service = UserService(db)
    
    # Check if user with email already exists
    existing_user = user_service.get_user_by_email(user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )
    
    # Check if user with username already exists
    existing_user = user_service.get_user_by_username(user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this username already exists"
        )
    
    # Create the user
    user = user_service.create_user(user_create)
    
    return APIResponse(content=user, message="User registered successfully")


@router.post("/login")
async def login_user(email: str, password: str, db: Session = Depends(get_db_session)):
    """Login a user and return access and refresh tokens."""
    auth_service = AuthenticationService(db)
    
    user = auth_service.authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access and refresh tokens
    access_token = auth_service.create_access_token_for_user(user)
    refresh_token = auth_service.create_refresh_token_for_user(user)
    
    return APIResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 15 * 60  # 15 minutes in seconds
        },
        message="Login successful"
    )


@router.post("/logout")
async def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Logout a user by revoking their refresh token."""
    auth_service = AuthenticationService(db)
    
    # In a real implementation, we would revoke the refresh token
    # For now, we'll just return a success message
    return APIResponse(message="Logged out successfully")


@router.get("/me", response_model=UserPublic)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Get the current user's profile."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return APIResponse(content=user, message="User profile retrieved successfully")


@router.put("/me", response_model=UserPublic)
async def update_current_user(
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Update the current user's profile."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Update the user
    user_service = UserService(db)
    updated_user = user_service.update_user(user.id, user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return APIResponse(content=updated_user, message="User profile updated successfully")