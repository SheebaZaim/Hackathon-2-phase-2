from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timedelta
from uuid import UUID
import uuid
from ..models.user import User
from ..models.auth_token import AuthenticationToken, TokenType
from ..auth.password import verify_password
from ..auth.token import create_access_token, create_refresh_token, verify_token
from ..auth.utils import verify_token as verify_credentials


class AuthenticationService:
    """Service class for authentication-related operations."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password."""
        statement = select(User).where(User.email == email)
        user = self.db_session.exec(statement).first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_access_token_for_user(self, user: User) -> str:
        """Create an access token for a user."""
        data = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username
        }
        # Access token valid for 15 minutes
        access_token = create_access_token(data=data, expires_delta=timedelta(minutes=15))
        return access_token
    
    def create_refresh_token_for_user(self, user: User) -> str:
        """Create a refresh token for a user."""
        data = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username
        }
        # Refresh token valid for 7 days
        refresh_token = create_refresh_token(data=data, expires_delta=timedelta(days=7))
        
        # Store refresh token in database
        token_record = AuthenticationToken(
            user_id=user.id,
            token_hash=refresh_token,
            token_type=TokenType.REFRESH
        )
        self.db_session.add(token_record)
        self.db_session.commit()
        
        return refresh_token
    
    def verify_access_token(self, token: str) -> Optional[dict]:
        """Verify an access token and return the payload."""
        try:
            payload = verify_token(token, token_type="access")
            return payload
        except Exception:
            return None
    
    def verify_refresh_token(self, token: str) -> Optional[dict]:
        """Verify a refresh token and return the payload."""
        try:
            payload = verify_token(token, token_type="refresh")
            return payload
        except Exception:
            return None
    
    def revoke_refresh_token(self, token: str) -> bool:
        """Revoke a refresh token."""
        # Find the token in the database
        statement = select(AuthenticationToken).where(
            AuthenticationToken.token_hash == token
        )
        token_record = self.db_session.exec(statement).first()
        
        if not token_record:
            return False
        
        # Mark the token as revoked
        token_record.revoked_at = datetime.utcnow()
        self.db_session.add(token_record)
        self.db_session.commit()
        
        return True
    
    def get_user_from_token(self, token: str) -> Optional[User]:
        """Get user from token payload."""
        payload = self.verify_access_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        statement = select(User).where(User.id == UUID(user_id))
        user = self.db_session.exec(statement).first()
        
        return user