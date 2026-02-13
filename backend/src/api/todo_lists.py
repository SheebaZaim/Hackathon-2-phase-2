"""TodoList CRUD API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from typing import List
from uuid import UUID

from ..models.todo_list import TodoList, TodoListCreate, TodoListUpdate, TodoListResponse
from ..services.todo_lists import TodoListService
from ..middleware.auth import get_current_user
from ..database.connection import get_session

router = APIRouter(prefix="/todo-lists", tags=["todo-lists"])


@router.get("", response_model=dict)
async def get_todo_lists(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of lists to return"),
    offset: int = Query(0, ge=0, description="Number of lists to skip"),
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all todo lists for authenticated user.
    Returns lists with task counts.
    """
    user_id = auth_data["user_id"]

    lists = TodoListService.get_lists(
        session=session,
        user_id=user_id,
        limit=limit,
        offset=offset
    )

    total = TodoListService.count_lists(
        session=session,
        user_id=user_id
    )

    # Convert to response format with task counts
    list_responses = []
    for todo_list in lists:
        task_count = TodoListService.count_tasks_in_list(session, todo_list.id)
        list_responses.append(
            TodoListResponse(
                id=todo_list.id,
                user_id=todo_list.user_id,
                name=todo_list.name,
                description=todo_list.description,
                color=todo_list.color,
                icon=todo_list.icon,
                is_default=todo_list.is_default,
                task_count=task_count,
                created_at=todo_list.created_at,
                updated_at=todo_list.updated_at
            )
        )

    return {
        "lists": list_responses,
        "total": total
    }


@router.post("", response_model=TodoListResponse, status_code=status.HTTP_201_CREATED)
async def create_todo_list(
    list_data: TodoListCreate,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new todo list for the authenticated user"""
    user_id = auth_data["user_id"]

    todo_list = TodoListService.create_list(
        session=session,
        user_id=user_id,
        list_data=list_data
    )

    task_count = TodoListService.count_tasks_in_list(session, todo_list.id)

    return TodoListResponse(
        id=todo_list.id,
        user_id=todo_list.user_id,
        name=todo_list.name,
        description=todo_list.description,
        color=todo_list.color,
        icon=todo_list.icon,
        is_default=todo_list.is_default,
        task_count=task_count,
        created_at=todo_list.created_at,
        updated_at=todo_list.updated_at
    )


@router.get("/{list_id}", response_model=TodoListResponse)
async def get_todo_list(
    list_id: UUID,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific todo list (must belong to authenticated user)"""
    user_id = auth_data["user_id"]

    todo_list = TodoListService.get_list(
        session=session,
        user_id=user_id,
        list_id=list_id
    )

    if not todo_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo list not found"
        )

    task_count = TodoListService.count_tasks_in_list(session, todo_list.id)

    return TodoListResponse(
        id=todo_list.id,
        user_id=todo_list.user_id,
        name=todo_list.name,
        description=todo_list.description,
        color=todo_list.color,
        icon=todo_list.icon,
        is_default=todo_list.is_default,
        task_count=task_count,
        created_at=todo_list.created_at,
        updated_at=todo_list.updated_at
    )


@router.put("/{list_id}", response_model=TodoListResponse)
async def update_todo_list(
    list_id: UUID,
    list_data: TodoListUpdate,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a todo list (must belong to authenticated user)"""
    user_id = auth_data["user_id"]

    todo_list = TodoListService.update_list(
        session=session,
        user_id=user_id,
        list_id=list_id,
        list_data=list_data
    )

    if not todo_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo list not found"
        )

    task_count = TodoListService.count_tasks_in_list(session, todo_list.id)

    return TodoListResponse(
        id=todo_list.id,
        user_id=todo_list.user_id,
        name=todo_list.name,
        description=todo_list.description,
        color=todo_list.color,
        icon=todo_list.icon,
        is_default=todo_list.is_default,
        task_count=task_count,
        created_at=todo_list.created_at,
        updated_at=todo_list.updated_at
    )


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_list(
    list_id: UUID,
    auth_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a todo list (must belong to authenticated user)
    Tasks in this list will have their todo_list_id set to NULL
    Cannot delete the only/default list
    """
    user_id = auth_data["user_id"]

    deleted = TodoListService.delete_list(
        session=session,
        user_id=user_id,
        list_id=list_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete list (either not found or it's the only/default list)"
        )

    return None  # 204 No Content
