from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid

from ..db import get_session
from ..models.subject_model import Subject, SubjectCreate, SubjectUpdate, SubjectResponse
from ..models.user_model import UserResponse
from ..middleware.jwt_middleware import get_current_user

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/", response_model=List[SubjectResponse])
def read_subjects(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all subjects (global for now, could be teacher-specific later)"""
    statement = select(Subject)
    subjects = session.exec(statement).all()
    return subjects


@router.post("/", response_model=SubjectResponse)
def create_subject(
    subject_data: SubjectCreate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new subject"""
    # Check if subject with same name or code already exists
    existing_subject = session.exec(
        select(Subject).where((Subject.name == subject_data.name) | (Subject.code == subject_data.code))
    ).first()
    
    if existing_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject with this name or code already exists"
        )
    
    # Create the subject
    subject_obj = Subject.from_orm(subject_data) if hasattr(Subject, 'from_orm') else Subject(**subject_data.dict())
    
    session.add(subject_obj)
    session.commit()
    session.refresh(subject_obj)
    
    return subject_obj


@router.get("/{subject_id}", response_model=SubjectResponse)
def read_subject(
    subject_id: uuid.UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific subject by ID"""
    statement = select(Subject).where(Subject.id == subject_id)
    subject = session.exec(statement).first()
    
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    return subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: uuid.UUID,
    subject_data: SubjectUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific subject"""
    statement = select(Subject).where(Subject.id == subject_id)
    subject = session.exec(statement).first()
    
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Check if new name or code conflicts with existing subjects
    if subject_data.name and subject_data.name != subject.name:
        existing_subject = session.exec(
            select(Subject).where(Subject.name == subject_data.name)
        ).first()
        
        if existing_subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject with this name already exists"
            )
    
    if subject_data.code and subject_data.code != subject.code:
        existing_subject = session.exec(
            select(Subject).where(Subject.code == subject_data.code)
        ).first()
        
        if existing_subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject with this code already exists"
            )
    
    # Update the subject with provided data
    update_data = subject_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subject, field, value)
    
    session.add(subject)
    session.commit()
    session.refresh(subject)
    
    return subject


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: uuid.UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific subject"""
    statement = select(Subject).where(Subject.id == subject_id)
    subject = session.exec(statement).first()
    
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Check if the subject is used by any results
    # This would require importing Result model and checking for references
    # For now, we'll skip this check but in a real implementation you'd want to verify
    # that no results reference this subject before deleting
    
    session.delete(subject)
    session.commit()
    
    return {"message": "Subject deleted successfully"}