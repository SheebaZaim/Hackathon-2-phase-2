"""Authentication endpoints for user registration and login"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
import hashlib
from jose import jwt
from datetime import datetime, timedelta
import os

from ..database.connection import get_session
from ..models.user import User
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password hashing
SALT = "todo_app_salt_2026"  # In production, use proper secret

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
    """Hash a password using SHA-256"""
    salted = f"{password}{SALT}".encode('utf-8')
    return hashlib.sha256(salted).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(plain_password) == hashed_password


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
