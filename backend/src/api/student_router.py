from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid

from ..db import get_session
from ..models.student_model import Student, StudentCreate, StudentUpdate, StudentResponse
from ..models.class_model import Class
from ..models.user_model import UserResponse
from ..middleware.jwt_middleware import get_current_user

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=List[StudentResponse])
def read_students(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all students for the current teacher's classes"""
    # First get all classes for the current teacher
    class_statement = select(Class.id).where(Class.teacher_id == current_user.id)
    class_ids = [row[0] for row in session.exec(class_statement)]
    
    if not class_ids:
        return []  # Return empty list if teacher has no classes
    
    # Then get all students in those classes
    statement = select(Student).where(Student.class_id.in_(class_ids))
    students = session.exec(statement).all()
    return students


@router.post("/", response_model=StudentResponse)
def create_student(
    student_data: StudentCreate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Add a new student to a class"""
    # Verify that the class belongs to the current teacher
    class_statement = select(Class).where(
        Class.id == student_data.class_id,
        Class.teacher_id == current_user.id
    )
    class_obj = session.exec(class_statement).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this class"
        )
    
    # Create the student
    student_obj = Student.from_orm(student_data) if hasattr(Student, 'from_orm') else Student(**student_data.dict())
    
    session.add(student_obj)
    session.commit()
    session.refresh(student_obj)
    
    return student_obj


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(
    student_id: uuid.UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific student by ID"""
    # Get the student and ensure they belong to a class owned by the current teacher
    statement = select(Student).join(Class).where(
        Student.id == student_id,
        Class.teacher_id == current_user.id
    )
    student = session.exec(statement).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: uuid.UUID,
    student_data: StudentUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific student"""
    # Get the student and ensure they belong to a class owned by the current teacher
    statement = select(Student).join(Class).where(
        Student.id == student_id,
        Class.teacher_id == current_user.id
    )
    student = session.exec(statement).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Update the student with provided data
    update_data = student_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    session.add(student)
    session.commit()
    session.refresh(student)
    
    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: uuid.UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Remove a student from a class"""
    # Get the student and ensure they belong to a class owned by the current teacher
    statement = select(Student).join(Class).where(
        Student.id == student_id,
        Class.teacher_id == current_user.id
    )
    student = session.exec(statement).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    session.delete(student)
    session.commit()
    
    return {"message": "Student removed successfully"}