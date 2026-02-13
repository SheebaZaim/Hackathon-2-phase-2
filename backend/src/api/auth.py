"""Authentication endpoints for user registration and login"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os

from ..database.connection import get_session
from ..models.user import User
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])

# JWT settings
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "supersecretdevelopmentkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def hash_password(password: str) -> str:
    """Hash a password using bcrypt (secure, generates unique salt per password)"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its bcrypt hash"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(user_id: uuid.UUID, email: str) -> str:
    """Create a JWT access token"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": email,
        "user_id": str(user_id),  # Convert UUID to string for JWT
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=TokenResponse)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_session)
):
    """Register a new user"""
    # Check if user already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = hash_password(request.password)
    new_user = User(
        email=request.email,
        password_hash=hashed_password,
        first_name="",
        last_name=""
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Create access token
    access_token = create_access_token(new_user.id, new_user.email)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
):
    """Login user"""
    # Find user
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Create access token
    access_token = create_access_token(user.id, user.email)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout():
    """
    Logout user (client-side token removal)
    Since we're using stateless JWT, logout is handled client-side by removing the token.
    This endpoint exists for API completeness and future session management.
    """
    return {"message": "Logged out successfully"}
