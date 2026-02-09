from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthenticationTokenBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    token_hash: str = Field(unique=True, nullable=False, max_length=255)
    token_type: TokenType = Field(default=TokenType.ACCESS, nullable=False)
    expires_at: datetime = Field(nullable=False)


class AuthenticationToken(AuthenticationTokenBase, table=True):
    """Authentication token model for the application."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked_at: Optional[datetime] = Field(default=None)


class AuthenticationTokenCreate(AuthenticationTokenBase):
    pass


class AuthenticationTokenUpdate(SQLModel):
    revoked_at: Optional[datetime] = None


class AuthenticationTokenPublic(AuthenticationTokenBase):
    id: uuid.UUID
    created_at: datetime
    revoked_at: Optional[datetime] = None