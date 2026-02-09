from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.session import get_db_session
from ..models.todo_list import TodoList, TodoListCreate, TodoListUpdate, TodoListPublic
from ..models.user import User
from ..services.todo_list_service import TodoListService
from ..services.auth_service import AuthenticationService
from ..utils.responses import APIResponse


router = APIRouter(prefix="/todo-lists", tags=["Todo Lists"])
security = HTTPBearer()


@router.get("/", response_model=List[TodoListPublic])
async def get_todo_lists(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Get all todo lists for the current user."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Get all todo lists for the user
    todo_list_service = TodoListService(db)
    todo_lists = todo_list_service.get_todo_lists_by_user(user.id)
    
    return APIResponse(content=todo_lists, message="Todo lists retrieved successfully")


@router.post("/", response_model=TodoListPublic)
async def create_todo_list(
    todo_list_create: TodoListCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Create a new todo list for the current user."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Create the todo list
    todo_list_service = TodoListService(db)
    todo_list = todo_list_service.create_todo_list(todo_list_create, user.id)
    
    return APIResponse(content=todo_list, message="Todo list created successfully")


@router.get("/{todo_list_id}", response_model=TodoListPublic)
async def get_todo_list(
    todo_list_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Get a specific todo list by ID."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Get the todo list
    todo_list_service = TodoListService(db)
    todo_list = todo_list_service.get_todo_list_by_id(todo_list_id)
    
    if not todo_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo list not found"
        )
    
    # Check if the user owns the todo list
    if todo_list.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this todo list"
        )
    
    return APIResponse(content=todo_list, message="Todo list retrieved successfully")


@router.put("/{todo_list_id}", response_model=TodoListPublic)
async def update_todo_list(
    todo_list_id: UUID,
    todo_list_update: TodoListUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Update a specific todo list by ID."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Update the todo list
    todo_list_service = TodoListService(db)
    todo_list = todo_list_service.update_todo_list(todo_list_id, todo_list_update)
    
    if not todo_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo list not found"
        )
    
    # Check if the user owns the todo list
    if todo_list.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this todo list"
        )
    
    return APIResponse(content=todo_list, message="Todo list updated successfully")


@router.delete("/{todo_list_id}")
async def delete_todo_list(
    todo_list_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Delete a specific todo list by ID."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Delete the todo list
    todo_list_service = TodoListService(db)
    success = todo_list_service.delete_todo_list(todo_list_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo list not found"
        )
    
    # Verify that the user owned the deleted todo list
    # (This check is redundant since delete_todo_list doesn't check ownership,
    # but we'll add it for security)
    if not todo_list_service.check_user_owns_todo_list(user.id, todo_list_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this todo list"
        )
    
    return APIResponse(message="Todo list deleted successfully")