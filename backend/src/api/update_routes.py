from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import asyncio

from ..models.verification_report import VerificationReport
from ..services.update_recommendation_engine import UpdateRecommendation, update_recommendation_engine
from ..services.verification_service import verification_service

router = APIRouter(prefix="/updates", tags=["updates"])


@router.get("/recommendations", summary="Get update recommendations")
async def get_update_recommendations():
    """
    Get recommendations for updating components based on verification results.
    """
    try:
        # Get the latest verification report
        latest_report = verification_service.get_latest_report()
        if not latest_report:
            raise HTTPException(status_code=404, detail="No verification reports found")
        
        # Generate recommendations from the report
        recommendations = await update_recommendation_engine.generate_recommendations_from_report(
            latest_report.components_checked
        )
        
        return {
            "recommendations": [rec.__dict__ for rec in recommendations],
            "count": len(recommendations),
            "generated_from_report": latest_report.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


@router.get("/recommendations-by-priority/{priority}", summary="Get recommendations by priority")
async def get_recommendations_by_priority(priority: str):
    """
    Get recommendations filtered by priority (critical, high, medium, low).
    """
    try:
        # Validate priority
        from ..services.update_recommendation_engine import RecommendationPriority
        try:
            priority_enum = RecommendationPriority(priority.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid priority: {priority}")
        
        # Get recommendations by priority
        recommendations = await update_recommendation_engine.get_recommendations_by_priority(priority_enum)
        
        return {
            "recommendations": [rec.__dict__ for rec in recommendations],
            "count": len(recommendations),
            "priority": priority
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recommendations: {str(e)}")


@router.get("/recommendations-by-type/{rec_type}", summary="Get recommendations by type")
async def get_recommendations_by_type(rec_type: str):
    """
    Get recommendations filtered by type (implementation, fix, configuration, optimization, security).
    """
    try:
        # Validate recommendation type
        from ..services.update_recommendation_engine import RecommendationType
        try:
            type_enum = RecommendationType(rec_type.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid recommendation type: {rec_type}")
        
        # Get recommendations by type
        recommendations = await update_recommendation_engine.get_recommendations_by_type(type_enum)
        
        return {
            "recommendations": [rec.__dict__ for rec in recommendations],
            "count": len(recommendations),
            "type": rec_type
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recommendations: {str(e)}")


@router.get("/top-recommendations", summary="Get top recommendations")
async def get_top_recommendations(count: int = 5):
    """
    Get the top N recommendations by priority.
    """
    try:
        recommendations = await update_recommendation_engine.get_top_recommendations(count)
        
        return {
            "recommendations": [rec.__dict__ for rec in recommendations],
            "count": len(recommendations),
            "requested_count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving top recommendations: {str(e)}")


@router.post("/apply-recommendation/{recommendation_id}", summary="Apply a recommendation")
async def apply_recommendation(recommendation_id: str):
    """
    Apply a specific recommendation (simulation).
    In a real implementation, this would trigger the actual update process.
    """
    try:
        # In a real implementation, this would apply the recommendation
        # For now, we'll return a simulated response
        return {
            "message": f"Recommendation {recommendation_id} has been applied (simulated)",
            "recommendation_id": recommendation_id,
            "status": "applied",
            "details": "This is a simulated response. In a real implementation, this would trigger the actual update process."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying recommendation: {str(e)}")


@router.get("/status", summary="Get update process status")
async def get_update_status():
    """
    Get the status of ongoing update processes.
    """
    try:
        # In a real implementation, this would track ongoing update processes
        # For now, we'll return a simulated status
        return {
            "status": "idle",
            "active_updates": 0,
            "pending_recommendations": 0,
            "last_update_check": "never",
            "details": "No active update processes. This is a simulated response."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving update status: {str(e)}")