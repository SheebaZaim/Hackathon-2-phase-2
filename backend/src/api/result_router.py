from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid

from ..db import get_session
from ..models.result_model import Result, ResultCreate, ResultUpdate, ResultResponse
from ..models.student_model import Student
from ..models.subject_model import Subject
from ..models.class_model import Class
from ..models.user_model import UserResponse
from ..middleware.jwt_middleware import get_current_user

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/", response_model=List[ResultResponse])
def read_results(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all results for students in the current teacher's classes"""
    # First get all classes for the current teacher
    class_statement = select(Class.id).where(Class.teacher_id == current_user.id)
    class_ids = [row[0] for row in session.exec(class_statement)]
    
    if not class_ids:
        return []  # Return empty list if teacher has no classes
    
    # Then get all students in those classes
    student_statement = select(Student.id).where(Student.class_id.in_(class_ids))
    student_ids = [row[0] for row in session.exec(student_statement)]
    
    if not student_ids:
        return []  # Return empty list if teacher has no students
    
    # Finally get all results for those students
    statement = select(Result).where(Result.student_id.in_(student_ids))
    results = session.exec(statement).all()
    return results


@router.post("/", response_model=ResultResponse)
def create_result(
    result_data: ResultCreate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Add a new result for a student"""
    # Verify that the student belongs to a class owned by the current teacher
    student_statement = select(Student).join(Class).where(
        Student.id == result_data.student_id,
        Class.teacher_id == current_user.id
    )
    student = session.exec(student_statement).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this student"
        )
    
    # Verify that the subject exists
    subject_statement = select(Subject).where(Subject.id == result_data.subject_id)
    subject = session.exec(subject_statement).first()
    
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Create the result
    result_obj = Result.from_orm(result_data) if hasattr(Result, 'from_orm') else Result(**result_data.dict())
    
    session.add(result_obj)
    session.commit()
    session.refresh(result_obj)
    
    return result_obj


@router.get("/{result_id}", response_model=ResultResponse)
def read_result(
    result_id: uuid.UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific result by ID"""
    # Get the result and ensure it belongs to a student in a class owned by the current teacher
    statement = select(Result).join(Student).join(Class).where(
        Result.id == result_id,
        Class.teacher_id == current_user.id
    )
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    return result


@router.put("/{result_id}", response_model=ResultResponse)
def update_result(
    result_id: uuid.UUID,
    result_data: ResultUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific result"""
    # Get the result and ensure it belongs to a student in a class owned by the current teacher
    statement = select(Result).join(Student).join(Class).where(
        Result.id == result_id,
        Class.teacher_id == current_user.id
    )
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    # Update the result with provided data
    update_data = result_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(result, field, value)
    
    session.add(result)
    session.commit()
    session.refresh(result)
    
    return result


@router.delete("/{result_id}")
def delete_result(
    result_id: uuid.UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific result"""
    # Get the result and ensure it belongs to a student in a class owned by the current teacher
    statement = select(Result).join(Student).join(Class).where(
        Result.id == result_id,
        Class.teacher_id == current_user.id
    )
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    session.delete(result)
    session.commit()
    
    return {"message": "Result deleted successfully"}