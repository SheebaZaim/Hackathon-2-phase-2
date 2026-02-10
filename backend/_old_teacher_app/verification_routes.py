from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import asyncio

from ..services.verification_service import verification_service
from ..models.verification_report import VerificationReport

router = APIRouter(prefix="/verification", tags=["verification"])


@router.get("/status", summary="Get current verification status")
async def get_verification_status():
    """
    Retrieves the current verification status of system components.
    """
    try:
        status_summary = verification_service.get_current_status_summary()
        return status_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving verification status: {str(e)}")


@router.get("/report/{report_id}", summary="Get detailed verification report")
async def get_verification_report(report_id: str):
    """
    Retrieves a detailed verification report by its ID.
    """
    try:
        report = verification_service.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail=f"Verification report with ID {report_id} not found")
        
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving verification report: {str(e)}")


@router.post("/run", summary="Initiate a new verification run")
async def run_verification(background_tasks: BackgroundTasks):
    """
    Initiates a new verification run in the background.
    """
    try:
        # Start the verification in the background
        report_id = await verification_service.run_full_verification()
        
        # In a real implementation, we would run this as a background task
        # For now, we'll return immediately with the report ID
        return {
            "message": "Verification process completed",
            "report_id": report_id,
            "estimated_duration": 0  # Since it's synchronous in this implementation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating verification: {str(e)}")


@router.get("/job/{job_id}", summary="Check status of a verification job")
async def get_verification_job_status(job_id: str):
    """
    Checks the status of a verification job.
    """
    try:
        job_status = verification_service.get_job_status(job_id)
        if not job_status:
            raise HTTPException(status_code=404, detail=f"Verification job with ID {job_id} not found")
        
        return job_status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job status: {str(e)}")


@router.get("/", summary="Get all verification reports")
async def get_verification_reports():
    """
    Retrieves a list of all verification reports.
    """
    try:
        reports = list(verification_service.reports.values())
        return {"reports": reports, "count": len(reports)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving verification reports: {str(e)}")


@router.get("/missing-components", summary="Get list of missing components")
async def get_missing_components():
    """
    Retrieves a list of components that are missing or incomplete.
    """
    try:
        from ..utils.component_detector import component_detector
        missing_components = component_detector.find_missing_expected_components()
        return {"missing_components": missing_components, "count": len(missing_components)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving missing components: {str(e)}")