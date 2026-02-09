from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from ..db import get_session
from ..models.school_planning_model import (
    SchoolPlanning, 
    SchoolPlanningCreate, 
    SchoolPlanningUpdate, 
    SchoolPlanningResponse
)
from ..middleware.jwt_middleware import get_current_user
from ..models.user_model import UserResponse

router = APIRouter(prefix="/plannings", tags=["plannings"])

@router.post("/", response_model=SchoolPlanningResponse)
def create_school_planning(
    planning_data: SchoolPlanningCreate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new school planning for the current user"""
    # Create new planning with the current user's ID
    planning = SchoolPlanning(
        **planning_data.dict(),
        user_id=current_user.id
    )
    
    session.add(planning)
    session.commit()
    session.refresh(planning)

    return SchoolPlanningResponse(
        id=planning.id,
        title=planning.title,
        description=planning.description,
        subject=planning.subject,
        grade_level=planning.grade_level,
        date=planning.date,
        duration=planning.duration,
        materials_needed=planning.materials_needed,
        learning_objectives=planning.learning_objectives,
        class_size=planning.class_size,
        teaching_method=planning.teaching_method,
        assessment_type=planning.assessment_type,
        standards_addressed=planning.standards_addressed,
        previous_knowledge_required=planning.previous_knowledge_required,
        extension_activities=planning.extension_activities,
        differentiation_strategies=planning.differentiation_strategies,
        resources_links=planning.resources_links,
        user_id=planning.user_id,
        created_at=planning.created_at,
        updated_at=planning.updated_at
    )


@router.get("/", response_model=List[SchoolPlanningResponse])
def read_school_plannings(
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all school plannings for the current user"""
    statement = select(SchoolPlanning).where(SchoolPlanning.user_id == current_user.id)
    plannings = session.exec(statement).all()
    
    result = []
    for planning in plannings:
        result.append(SchoolPlanningResponse(
            id=planning.id,
            title=planning.title,
            description=planning.description,
            subject=planning.subject,
            grade_level=planning.grade_level,
            date=planning.date,
            duration=planning.duration,
            materials_needed=planning.materials_needed,
            learning_objectives=planning.learning_objectives,
            class_size=planning.class_size,
            teaching_method=planning.teaching_method,
            assessment_type=planning.assessment_type,
            standards_addressed=planning.standards_addressed,
            previous_knowledge_required=planning.previous_knowledge_required,
            extension_activities=planning.extension_activities,
            differentiation_strategies=planning.differentiation_strategies,
            resources_links=planning.resources_links,
            user_id=planning.user_id,
            created_at=planning.created_at,
            updated_at=planning.updated_at
        ))
    return result


@router.get("/{planning_id}", response_model=SchoolPlanningResponse)
def read_school_planning(
    planning_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific school planning by ID for the current user"""
    statement = select(SchoolPlanning).where(
        SchoolPlanning.id == planning_id,
        SchoolPlanning.user_id == current_user.id
    )
    planning = session.exec(statement).first()
    
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School planning not found"
        )
    
    return SchoolPlanningResponse(
        id=planning.id,
        title=planning.title,
        description=planning.description,
        subject=planning.subject,
        grade_level=planning.grade_level,
        date=planning.date,
        duration=planning.duration,
        materials_needed=planning.materials_needed,
        learning_objectives=planning.learning_objectives,
        class_size=planning.class_size,
        teaching_method=planning.teaching_method,
        assessment_type=planning.assessment_type,
        standards_addressed=planning.standards_addressed,
        previous_knowledge_required=planning.previous_knowledge_required,
        extension_activities=planning.extension_activities,
        differentiation_strategies=planning.differentiation_strategies,
        resources_links=planning.resources_links,
        user_id=planning.user_id,
        created_at=planning.created_at,
        updated_at=planning.updated_at
    )


@router.put("/{planning_id}", response_model=SchoolPlanningResponse)
def update_school_planning(
    planning_id: UUID,
    planning_data: SchoolPlanningUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific school planning for the current user"""
    statement = select(SchoolPlanning).where(
        SchoolPlanning.id == planning_id,
        SchoolPlanning.user_id == current_user.id
    )
    planning = session.exec(statement).first()
    
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School planning not found"
        )
    
    # Update the planning with the new data
    for field, value in planning_data.dict(exclude_unset=True).items():
        setattr(planning, field, value)
    
    session.add(planning)
    session.commit()
    session.refresh(planning)
    
    return SchoolPlanningResponse(
        id=planning.id,
        title=planning.title,
        description=planning.description,
        subject=planning.subject,
        grade_level=planning.grade_level,
        date=planning.date,
        duration=planning.duration,
        materials_needed=planning.materials_needed,
        learning_objectives=planning.learning_objectives,
        class_size=planning.class_size,
        teaching_method=planning.teaching_method,
        assessment_type=planning.assessment_type,
        standards_addressed=planning.standards_addressed,
        previous_knowledge_required=planning.previous_knowledge_required,
        extension_activities=planning.extension_activities,
        differentiation_strategies=planning.differentiation_strategies,
        resources_links=planning.resources_links,
        user_id=planning.user_id,
        created_at=planning.created_at,
        updated_at=planning.updated_at
    )


@router.delete("/{planning_id}")
def delete_school_planning(
    planning_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific school planning for the current user"""
    statement = select(SchoolPlanning).where(
        SchoolPlanning.id == planning_id,
        SchoolPlanning.user_id == current_user.id
    )
    planning = session.exec(statement).first()
    
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School planning not found"
        )
    
    session.delete(planning)
    session.commit()
    
    return {"message": "School planning deleted successfully"}