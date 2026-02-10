from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from typing import Optional
from ..models.user_model import User, UserCreate, UserResponse

# Password hashing context - using multiple schemes as fallback
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto",
                         bcrypt__rounds=12,
                         argon2__rounds=3,
                         argon2__memory_cost=65536,
                         argon2__parallelism=4)

# Get secret from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_development")
ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Hash a plaintext password with length check"""
    # Check password length to avoid bcrypt limitations
    if len(password) > 72:
        password = password[:72]  # Truncate if too long for bcrypt

    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error hashing password: {e}")
        # Fallback to argon2 only if bcrypt fails
        from passlib.hash import argon2
        return argon2.hash(password)

def authenticate_user(user: User, password: str) -> bool:
    """Authenticate a user by verifying their password"""
    if not user or not verify_password(password, user.password_hash):
        return False
    return True

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default 15 minutes
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new refresh token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # Default 7 days
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify a JWT token and return the payload"""
    from jose import JWTError
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_user_response(user: User) -> UserResponse:
    """Create a UserResponse object from a User model"""
    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at
    )