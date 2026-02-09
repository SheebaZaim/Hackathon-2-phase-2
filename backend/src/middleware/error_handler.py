from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from ..config.logging import get_logger
import traceback


logger = get_logger(__name__)


class ErrorHandlingMiddleware:
    """Custom error handling middleware."""
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        try:
            response = await self.app(scope, receive, send)
            return response
        except HTTPException as e:
            # Log the HTTP exception
            logger.warning(f"HTTP Exception: {e.status_code} - {e.detail}")
            
            # Return JSON response for HTTP exceptions
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "detail": e.detail,
                    "error_code": getattr(e, 'error_code', 'HTTP_ERROR'),
                    "timestamp": request.headers.get('date', '')
                }
            )
        except Exception as e:
            # Log the unexpected exception with traceback
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            
            # Return generic error response for unexpected errors
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error_code": "INTERNAL_ERROR",
                    "timestamp": request.headers.get('date', ''),
                    "traceback": traceback.format_exc() if __name__ == "__main__" else None
                }
            )


async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "timestamp": request.headers.get('date', '')
        }
    )