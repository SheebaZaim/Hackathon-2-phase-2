from typing import Any, Dict, Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime


def create_success_response(
    data: Any = None, 
    message: str = "Success", 
    status_code: int = 200
) -> Dict[str, Any]:
    """Create a standardized success response."""
    response = {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return response


def create_error_response(
    detail: str, 
    error_code: str = "GENERIC_ERROR", 
    status_code: int = 400
) -> Dict[str, Any]:
    """Create a standardized error response."""
    response = {
        "success": False,
        "error": {
            "detail": detail,
            "error_code": error_code,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }
    return response


def create_paginated_response(
    data: list, 
    page: int, 
    size: int, 
    total: int
) -> Dict[str, Any]:
    """Create a standardized paginated response."""
    total_pages = (total + size - 1) // size  # Ceiling division
    
    response = {
        "data": data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return response


class APIResponse(JSONResponse):
    """Custom JSONResponse class for API responses."""
    
    def __init__(
        self, 
        content: Any = None, 
        status_code: int = 200,
        message: Optional[str] = None,
        error_detail: Optional[str] = None,
        **kwargs
    ):
        if error_detail:
            content = create_error_response(error_detail, status_code=status_code)
            if status_code >= 400:
                super().__init__(content, status_code=status_code, **kwargs)
            else:
                # Use 400 as default for error responses
                super().__init__(content, status_code=400, **kwargs)
        else:
            content = create_success_response(content, message or "Success", status_code)
            super().__init__(content, status_code=status_code, **kwargs)


def raise_http_exception(
    status_code: int, 
    detail: str, 
    error_code: str = "GENERIC_ERROR"
):
    """Raise an HTTP exception with standardized error format."""
    raise HTTPException(
        status_code=status_code,
        detail=create_error_response(detail, error_code, status_code)
    )