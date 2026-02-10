from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserUpdate
from ..auth.password import get_password_hash
from uuid import UUID


class UserService:
    """Service class for user-related operations."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Retrieve a user by their ID."""
        statement = select(User).where(User.id == user_id)
        return self.db_session.exec(statement).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email."""
        statement = select(User).where(User.email == email)
        return self.db_session.exec(statement).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        statement = select(User).where(User.username == username)
        return self.db_session.exec(statement).first()
    
    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        # Hash the password
        hashed_password = get_password_hash(user_create.password)
        
        # Create the user object
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password
        )
        
        # Add to session and commit
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        
        return db_user
    
    def update_user(self, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        """Update an existing user."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        # Update fields if they are provided
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.first_name is not None:
            db_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            db_user.last_name = user_update.last_name
        if user_update.password is not None:
            db_user.hashed_password = get_password_hash(user_update.password)
        
        # Commit changes
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        
        return db_user
    
    def delete_user(self, user_id: UUID) -> bool:
        """Delete a user."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False
        
        self.db_session.delete(db_user)
        self.db_session.commit()
        return True
    
    def activate_user(self, user_id: UUID) -> Optional[User]:
        """Activate a user account."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        db_user.is_active = True
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        
        return db_user
    
    def deactivate_user(self, user_id: UUID) -> Optional[User]:
        """Deactivate a user account."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        db_user.is_active = False
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        
        return db_user