from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid

from ..db import get_session
from ..models.class_model import Class, ClassCreate, ClassUpdate, ClassResponse
from ..models.user_model import UserResponse
from ..middleware.jwt_middleware import get_current_user

router = APIRouter(prefix="/classes", tags=["classes"])

@router.get("/", response_model=List[ClassResponse])
def read_classes(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all classes for the current teacher"""
    statement = select(Class).where(Class.teacher_id == current_user.id)
    classes = session.exec(statement).all()
    return classes


@router.post("/", response_model=ClassResponse)
def create_class(
    class_data: ClassCreate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new class for the current teacher"""
    # Create class with the current user as the teacher
    class_obj = Class.from_orm(class_data) if hasattr(Class, 'from_orm') else Class(**class_data.dict())
    class_obj.teacher_id = current_user.id
    
    session.add(class_obj)
    session.commit()
    session.refresh(class_obj)
    
    return class_obj


@router.get("/{class_id}", response_model=ClassResponse)
def read_class(
    class_id: uuid.UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific class by ID"""
    statement = select(Class).where(Class.id == class_id, Class.teacher_id == current_user.id)
    class_obj = session.exec(statement).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    return class_obj


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
    class_id: uuid.UUID,
    class_data: ClassUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific class"""
    statement = select(Class).where(Class.id == class_id, Class.teacher_id == current_user.id)
    class_obj = session.exec(statement).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Update the class with provided data
    update_data = class_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(class_obj, field, value)
    
    session.add(class_obj)
    session.commit()
    session.refresh(class_obj)
    
    return class_obj


@router.delete("/{class_id}")
def delete_class(
    class_id: uuid.UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific class"""
    statement = select(Class).where(Class.id == class_id, Class.teacher_id == current_user.id)
    class_obj = session.exec(statement).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    session.delete(class_obj)
    session.commit()
    
    return {"message": "Class deleted successfully"}