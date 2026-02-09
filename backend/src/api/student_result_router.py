from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from ..db import get_session
from ..models.student_result_model import (
    StudentResult, 
    StudentResultCreate, 
    StudentResultUpdate, 
    StudentResultResponse
)
from ..middleware.jwt_middleware import get_current_user
from ..models.user_model import UserResponse

router = APIRouter(prefix="/results", tags=["results"])

@router.post("/", response_model=StudentResultResponse)
def create_student_result(
    result_data: StudentResultCreate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new student result for the current user"""
    # Calculate percentage if max_score is provided
    percentage = None
    if result_data.max_score and result_data.max_score > 0:
        percentage = (result_data.score / result_data.max_score) * 100
    
    # Determine grade letter based on percentage
    grade_letter = None
    if percentage is not None:
        if percentage >= 90:
            grade_letter = "A"
        elif percentage >= 80:
            grade_letter = "B"
        elif percentage >= 70:
            grade_letter = "C"
        elif percentage >= 60:
            grade_letter = "D"
        else:
            grade_letter = "F"
    
    # Create new result with the current user's ID
    result = StudentResult(
        **result_data.dict(),
        user_id=current_user.id,
        percentage=percentage,
        grade_letter=grade_letter
    )
    
    session.add(result)
    session.commit()
    session.refresh(result)

    return StudentResultResponse(
        id=result.id,
        student_name=result.student_name,
        assignment_title=result.assignment_title,
        score=result.score,
        max_score=result.max_score,
        percentage=result.percentage,
        grade_letter=result.grade_letter,
        subject=result.subject,
        date_recorded=result.date_recorded,
        comments=result.comments,
        user_id=result.user_id,
        created_at=result.created_at,
        updated_at=result.updated_at
    )


@router.get("/", response_model=List[StudentResultResponse])
def read_student_results(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all student results for the current user"""
    statement = select(StudentResult).where(StudentResult.user_id == current_user.id)
    results = session.exec(statement).all()
    
    result_list = []
    for result in results:
        result_list.append(StudentResultResponse(
            id=result.id,
            student_name=result.student_name,
            assignment_title=result.assignment_title,
            score=result.score,
            max_score=result.max_score,
            percentage=result.percentage,
            grade_letter=result.grade_letter,
            subject=result.subject,
            date_recorded=result.date_recorded,
            comments=result.comments,
            user_id=result.user_id,
            created_at=result.created_at,
            updated_at=result.updated_at
        ))
    return result_list


@router.get("/{result_id}", response_model=StudentResultResponse)
def read_student_result(
    result_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific student result by ID for the current user"""
    statement = select(StudentResult).where(
        StudentResult.id == result_id,
        StudentResult.user_id == current_user.id
    )
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student result not found"
        )
    
    return StudentResultResponse(
        id=result.id,
        student_name=result.student_name,
        assignment_title=result.assignment_title,
        score=result.score,
        max_score=result.max_score,
        percentage=result.percentage,
        grade_letter=result.grade_letter,
        subject=result.subject,
        date_recorded=result.date_recorded,
        comments=result.comments,
        user_id=result.user_id,
        created_at=result.created_at,
        updated_at=result.updated_at
    )


@router.put("/{result_id}", response_model=StudentResultResponse)
def update_student_result(
    result_id: UUID,
    result_data: StudentResultUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific student result for the current user"""
    statement = select(StudentResult).where(
        StudentResult.id == result_id,
        StudentResult.user_id == current_user.id
    )
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student result not found"
        )
    
    # Update the result with the new data
    for field, value in result_data.dict(exclude_unset=True).items():
        setattr(result, field, value)
    
    # Recalculate percentage and grade if score/max_score changed
    if result_data.score is not None or result_data.max_score is not None:
        score = result_data.score if result_data.score is not None else result.score
        max_score = result_data.max_score if result_data.max_score is not None else result.max_score
        
        if max_score and max_score > 0:
            result.percentage = (score / max_score) * 100
            # Determine grade letter based on percentage
            if result.percentage >= 90:
                result.grade_letter = "A"
            elif result.percentage >= 80:
                result.grade_letter = "B"
            elif result.percentage >= 70:
                result.grade_letter = "C"
            elif result.percentage >= 60:
                result.grade_letter = "D"
            else:
                result.grade_letter = "F"
    
    session.add(result)
    session.commit()
    session.refresh(result)
    
    return StudentResultResponse(
        id=result.id,
        student_name=result.student_name,
        assignment_title=result.assignment_title,
        score=result.score,
        max_score=result.max_score,
        percentage=result.percentage,
        grade_letter=result.grade_letter,
        subject=result.subject,
        date_recorded=result.date_recorded,
        comments=result.comments,
        user_id=result.user_id,
        created_at=result.created_at,
        updated_at=result.updated_at
    )


@router.delete("/{result_id}")
def delete_student_result(
    result_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific student result for the current user"""
    statement = select(StudentResult).where(
        StudentResult.id == result_id,
        StudentResult.user_id == current_user.id
    )
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student result not found"
        )
    
    session.delete(result)
    session.commit()
    
    return {"message": "Student result deleted successfully"}