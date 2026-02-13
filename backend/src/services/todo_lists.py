"""Service layer for TodoList operations"""
from sqlmodel import Session, select, func
from typing import List, Optional
from uuid import UUID

from ..models.todo_list import TodoList, TodoListCreate, TodoListUpdate
from ..models.task import Task


class TodoListService:
    """Service class for todo list operations"""

    @staticmethod
    def get_lists(
        session: Session,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[TodoList]:
        """Get all todo lists for a user"""
        statement = (
            select(TodoList)
            .where(TodoList.user_id == user_id)
            .order_by(TodoList.is_default.desc(), TodoList.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        lists = session.exec(statement).all()
        return lists

    @staticmethod
    def count_lists(session: Session, user_id: UUID) -> int:
        """Count total todo lists for a user"""
        statement = (
            select(func.count(TodoList.id))
            .where(TodoList.user_id == user_id)
        )
        count = session.exec(statement).one()
        return count

    @staticmethod
    def get_list(session: Session, user_id: UUID, list_id: UUID) -> Optional[TodoList]:
        """Get a specific todo list"""
        statement = (
            select(TodoList)
            .where(TodoList.id == list_id, TodoList.user_id == user_id)
        )
        todo_list = session.exec(statement).first()
        return todo_list

    @staticmethod
    def count_tasks_in_list(session: Session, list_id: UUID) -> int:
        """Count tasks in a specific list"""
        statement = (
            select(func.count(Task.id))
            .where(Task.todo_list_id == list_id)
        )
        count = session.exec(statement).one()
        return count

    @staticmethod
    def create_list(
        session: Session,
        user_id: UUID,
        list_data: TodoListCreate
    ) -> TodoList:
        """Create a new todo list"""
        # If this is set as default, unset other defaults
        if list_data.is_default:
            statement = (
                select(TodoList)
                .where(TodoList.user_id == user_id, TodoList.is_default == True)
            )
            existing_defaults = session.exec(statement).all()
            for existing in existing_defaults:
                existing.is_default = False
                session.add(existing)

        new_list = TodoList(
            user_id=user_id,
            name=list_data.name,
            description=list_data.description,
            color=list_data.color,
            icon=list_data.icon,
            is_default=list_data.is_default or False
        )

        session.add(new_list)
        session.commit()
        session.refresh(new_list)
        return new_list

    @staticmethod
    def update_list(
        session: Session,
        user_id: UUID,
        list_id: UUID,
        list_data: TodoListUpdate
    ) -> Optional[TodoList]:
        """Update a todo list"""
        todo_list = TodoListService.get_list(session, user_id, list_id)
        if not todo_list:
            return None

        # If setting as default, unset other defaults
        if list_data.is_default:
            statement = (
                select(TodoList)
                .where(
                    TodoList.user_id == user_id,
                    TodoList.is_default == True,
                    TodoList.id != list_id
                )
            )
            existing_defaults = session.exec(statement).all()
            for existing in existing_defaults:
                existing.is_default = False
                session.add(existing)

        # Update fields
        if list_data.name is not None:
            todo_list.name = list_data.name
        if list_data.description is not None:
            todo_list.description = list_data.description
        if list_data.color is not None:
            todo_list.color = list_data.color
        if list_data.icon is not None:
            todo_list.icon = list_data.icon
        if list_data.is_default is not None:
            todo_list.is_default = list_data.is_default

        from datetime import datetime
        todo_list.updated_at = datetime.utcnow()

        session.add(todo_list)
        session.commit()
        session.refresh(todo_list)
        return todo_list

    @staticmethod
    def delete_list(session: Session, user_id: UUID, list_id: UUID) -> bool:
        """Delete a todo list (tasks will have their todo_list_id set to NULL)"""
        todo_list = TodoListService.get_list(session, user_id, list_id)
        if not todo_list:
            return False

        # Don't allow deleting the only/default list
        if todo_list.is_default:
            total_lists = TodoListService.count_lists(session, user_id)
            if total_lists == 1:
                return False  # Can't delete the only list

        session.delete(todo_list)
        session.commit()
        return True
