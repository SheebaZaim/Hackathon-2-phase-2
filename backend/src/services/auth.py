"""Authentication service for JWT verification"""
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secret from environment - MUST match frontend
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"


def verify_jwt_token(token: str) -> dict:
    """
    Verify JWT token and return payload.

    Args:
        token: JWT token string

    Returns:
        dict: Token payload with user info

    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTError(f"Invalid token: {str(e)}")


def extract_user_id(token: str) -> str:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        str: User ID from token

    Raises:
        JWTError: If token is invalid or user_id not found
    """
    payload = verify_jwt_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise JWTError("User ID not found in token")

    return user_id
