from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID
from ..models.todo_list import TodoList, TodoListCreate, TodoListUpdate
from ..models.user import User


class TodoListService:
    """Service class for todo list-related operations."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_todo_list_by_id(self, todo_list_id: UUID) -> Optional[TodoList]:
        """Retrieve a todo list by its ID."""
        statement = select(TodoList).where(TodoList.id == todo_list_id)
        return self.db_session.exec(statement).first()
    
    def get_todo_lists_by_user(self, user_id: UUID) -> List[TodoList]:
        """Retrieve all todo lists for a specific user."""
        statement = select(TodoList).where(TodoList.user_id == user_id)
        return self.db_session.exec(statement).all()
    
    def create_todo_list(self, todo_list_create: TodoListCreate, user_id: UUID) -> TodoList:
        """Create a new todo list for a user."""
        db_todo_list = TodoList(
            title=todo_list_create.title,
            description=todo_list_create.description,
            is_public=todo_list_create.is_public,
            user_id=user_id,
            position=todo_list_create.position
        )
        
        self.db_session.add(db_todo_list)
        self.db_session.commit()
        self.db_session.refresh(db_todo_list)
        
        return db_todo_list
    
    def update_todo_list(self, todo_list_id: UUID, todo_list_update: TodoListUpdate) -> Optional[TodoList]:
        """Update an existing todo list."""
        db_todo_list = self.get_todo_list_by_id(todo_list_id)
        if not db_todo_list:
            return None
        
        # Update fields if they are provided
        if todo_list_update.title is not None:
            db_todo_list.title = todo_list_update.title
        if todo_list_update.description is not None:
            db_todo_list.description = todo_list_update.description
        if todo_list_update.is_public is not None:
            db_todo_list.is_public = todo_list_update.is_public
        if todo_list_update.position is not None:
            db_todo_list.position = todo_list_update.position
        
        self.db_session.add(db_todo_list)
        self.db_session.commit()
        self.db_session.refresh(db_todo_list)
        
        return db_todo_list
    
    def delete_todo_list(self, todo_list_id: UUID) -> bool:
        """Delete a todo list."""
        db_todo_list = self.get_todo_list_by_id(todo_list_id)
        if not db_todo_list:
            return False
        
        self.db_session.delete(db_todo_list)
        self.db_session.commit()
        return True
    
    def check_user_owns_todo_list(self, user_id: UUID, todo_list_id: UUID) -> bool:
        """Check if a user owns a specific todo list."""
        statement = select(TodoList).where(
            TodoList.id == todo_list_id,
            TodoList.user_id == user_id
        )
        todo_list = self.db_session.exec(statement).first()
        return todo_list is not None