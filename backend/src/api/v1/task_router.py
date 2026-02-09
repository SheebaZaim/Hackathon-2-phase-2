from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.session import get_db_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from ..models.todo_list import TodoList
from ..services.task_service import TaskService
from ..services.todo_list_service import TodoListService
from ..services.auth_service import AuthenticationService
from ..utils.responses import APIResponse


router = APIRouter(prefix="/tasks", tags=["Tasks"])
security = HTTPBearer()


@router.get("/todo-lists/{todo_list_id}", response_model=List[TaskPublic])
async def get_tasks_by_todo_list(
    todo_list_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Get all tasks for a specific todo list."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Verify that the user owns the todo list
    todo_list_service = TodoListService(db)
    if not todo_list_service.check_user_owns_todo_list(user.id, todo_list_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this todo list"
        )
    
    # Get all tasks for the todo list
    task_service = TaskService(db)
    tasks = task_service.get_tasks_by_todo_list(todo_list_id)
    
    return APIResponse(content=tasks, message="Tasks retrieved successfully")


@router.post("/todo-lists/{todo_list_id}", response_model=TaskPublic)
async def create_task(
    todo_list_id: UUID,
    task_create: TaskCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Create a new task in a specific todo list."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Verify that the user owns the todo list
    todo_list_service = TodoListService(db)
    if not todo_list_service.check_user_owns_todo_list(user.id, todo_list_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to add tasks to this todo list"
        )
    
    # Create the task
    task_service = TaskService(db)
    task = task_service.create_task(task_create, todo_list_id)
    
    return APIResponse(content=task, message="Task created successfully")


@router.get("/{task_id}", response_model=TaskPublic)
async def get_task(
    task_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Get a specific task by ID."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Get the task
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify that the user owns the todo list that contains the task
    if not task_service.check_todo_list_owns_task(task.todo_list_id, task_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this task"
        )
    
    # Verify that the user owns the todo list that contains the task
    todo_list_service = TodoListService(db)
    if not todo_list_service.check_user_owns_todo_list(user.id, task.todo_list_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this task"
        )
    
    return APIResponse(content=task, message="Task retrieved successfully")


@router.put("/{task_id}", response_model=TaskPublic)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Update a specific task by ID."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Update the task
    task_service = TaskService(db)
    task = task_service.update_task(task_id, task_update)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify that the user owns the todo list that contains the task
    todo_list_service = TodoListService(db)
    if not todo_list_service.check_user_owns_todo_list(user.id, task.todo_list_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task"
        )
    
    return APIResponse(content=task, message="Task updated successfully")


@router.patch("/{task_id}/toggle-completion", response_model=TaskPublic)
async def toggle_task_completion(
    task_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Toggle the completion status of a specific task."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Toggle the task completion
    task_service = TaskService(db)
    task = task_service.toggle_task_completion(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify that the user owns the todo list that contains the task
    todo_list_service = TodoListService(db)
    if not todo_list_service.check_user_owns_todo_list(user.id, task.todo_list_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task"
        )
    
    return APIResponse(content=task, message="Task completion status updated successfully")


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Delete a specific task by ID."""
    auth_service = AuthenticationService(db)
    
    # Verify the token and get the user
    user = auth_service.get_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Delete the task
    task_service = TaskService(db)
    success = task_service.delete_task(task_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify that the user owned the deleted task
    # (This check is redundant since delete_task doesn't check ownership,
    # but we'll add it for security)
    if not task_service.check_todo_list_owns_task(task.todo_list_id, task_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task"
        )
    
    # Verify that the user owns the todo list that contained the task
    todo_list_service = TodoListService(db)
    if not todo_list_service.check_user_owns_todo_list(user.id, task.todo_list_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task"
        )
    
    return APIResponse(message="Task deleted successfully")