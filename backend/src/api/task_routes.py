from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from ..models.task_template import TaskTemplate
from ..services.task_generator import task_generator
from ..services.verification_service import verification_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", summary="Get all tasks")
async def get_tasks(
    status: Optional[str] = Query(None, description="Filter tasks by status"),
    priority: Optional[str] = Query(None, description="Filter tasks by priority"),
    assignee: Optional[str] = Query(None, description="Filter tasks by assignee"),
    tag: Optional[str] = Query(None, description="Filter tasks by tag")
):
    """
    Retrieve all tasks with optional filters.
    """
    try:
        # In a real implementation, we would have a task repository to store and retrieve tasks
        # For now, we'll return an empty list since we don't have a persistent task store
        # But we can generate tasks from a verification report if provided
        
        # This is a simplified implementation - in reality, you'd have a database of tasks
        # For demonstration, we'll return an empty list
        return {"tasks": [], "count": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")


@router.get("/generate-from-report/{report_id}", summary="Generate tasks from verification report")
async def generate_tasks_from_report(report_id: str):
    """
    Generate implementation tasks based on a verification report.
    """
    try:
        # Generate tasks from the verification report
        tasks = task_generator.generate_tasks_from_verification_report(report_id)
        
        return {
            "tasks": [task.dict() for task in tasks],
            "count": len(tasks),
            "generated_at": datetime.utcnow().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating tasks: {str(e)}")


@router.post("/", summary="Create a new task")
async def create_task(task: TaskTemplate):
    """
    Create a new task.
    """
    try:
        # In a real implementation, we would save the task to a database
        # For now, we'll just return the task as if it was created
        # Update the timestamps
        task.updated_at = datetime.utcnow()
        
        return {
            "task": task.dict(),
            "message": "Task created successfully (simulation)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


@router.get("/{task_id}", summary="Get a specific task")
async def get_task(task_id: str):
    """
    Retrieve a specific task by ID.
    """
    try:
        # In a real implementation, we would fetch the task from a database
        # For now, we'll return an error since we don't have persistent tasks
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")


@router.put("/{task_id}", summary="Update a task")
async def update_task(task_id: str, task: TaskTemplate):
    """
    Update an existing task.
    """
    try:
        # In a real implementation, we would update the task in a database
        # For now, we'll return an error since we don't have persistent tasks
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


@router.delete("/{task_id}", summary="Delete a task")
async def delete_task(task_id: str):
    """
    Delete a task.
    """
    try:
        # In a real implementation, we would delete the task from a database
        # For now, we'll return an error since we don't have persistent tasks
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")


@router.post("/generate-constitution-tasks", summary="Generate tasks for constitution compliance")
async def generate_constitution_tasks():
    """
    Generate tasks for constitution compliance issues.
    """
    try:
        # Generate tasks for constitution compliance issues
        tasks = task_generator.generate_tasks_for_constitution_issues()
        
        return {
            "tasks": [task.dict() for task in tasks],
            "count": len(tasks),
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating constitution tasks: {str(e)}")