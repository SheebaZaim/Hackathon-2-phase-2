from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, select, create_engine
from typing import Optional
from datetime import datetime
import os
from enum import Enum

# Define approval status enum
class ApprovalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

# Admin dashboard models
class AdminTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    user_email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approval_status: ApprovalStatus = Field(default=ApprovalStatus.pending)
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

class AdminUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Create app for admin dashboard
app = FastAPI(title="Admin Dashboard", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(bind=engine)

# Admin dashboard endpoints
@app.get("/")
def admin_home():
    return {"message": "Admin Dashboard - Task Approval System"}

@app.get("/api/admin/pending-tasks")
def get_pending_tasks(session: Session = Depends(get_session)):
    """Get all pending tasks awaiting approval"""
    statement = select(AdminTask).where(AdminTask.approval_status == ApprovalStatus.pending)
    tasks = session.exec(statement).all()
    return tasks

@app.get("/api/admin/approved-tasks")
def get_approved_tasks(session: Session = Depends(get_session)):
    """Get all approved tasks"""
    statement = select(AdminTask).where(AdminTask.approval_status == ApprovalStatus.approved)
    tasks = session.exec(statement).all()
    return tasks

@app.get("/api/admin/rejected-tasks")
def get_rejected_tasks(session: Session = Depends(get_session)):
    """Get all rejected tasks"""
    statement = select(AdminTask).where(AdminTask.approval_status == ApprovalStatus.rejected)
    tasks = session.exec(statement).all()
    return tasks

@app.put("/api/admin/tasks/{task_id}/approve")
def approve_task(task_id: int, approver_email: str, session: Session = Depends(get_session)):
    """Approve a task"""
    task = session.get(AdminTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.approval_status = ApprovalStatus.approved
    task.approved_by = approver_email
    task.approved_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@app.put("/api/admin/tasks/{task_id}/reject")
def reject_task(task_id: int, reason: Optional[str] = None, session: Session = Depends(get_session)):
    """Reject a task"""
    task = session.get(AdminTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.approval_status = ApprovalStatus.rejected
    # Add rejection reason to description if provided
    if reason:
        if task.description:
            task.description += f" [REJECTED: {reason}]"
        else:
            task.description = f"[REJECTED: {reason}]"

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@app.delete("/api/admin/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Permanently delete a task"""
    task = session.get(AdminTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}

@app.get("/api/admin/stats")
def get_approval_stats(session: Session = Depends(get_session)):
    """Get approval statistics"""
    statement_pending = select(AdminTask).where(AdminTask.approval_status == ApprovalStatus.pending)
    statement_approved = select(AdminTask).where(AdminTask.approval_status == ApprovalStatus.approved)
    statement_rejected = select(AdminTask).where(AdminTask.approval_status == ApprovalStatus.rejected)

    pending_tasks = session.exec(statement_pending).all()
    approved_tasks = session.exec(statement_approved).all()
    rejected_tasks = session.exec(statement_rejected).all()

    return {
        "total_pending": len(pending_tasks),
        "total_approved": len(approved_tasks),
        "total_rejected": len(rejected_tasks),
        "total_tasks": len(pending_tasks) + len(approved_tasks) + len(rejected_tasks)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)