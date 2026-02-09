from fastapi.middleware.cors import CORSMiddleware
from typing import List


def add_cors_middleware(app, 
                       allow_origins: List[str] = None,
                       allow_credentials: bool = True,
                       allow_methods: List[str] = ["*"],
                       allow_headers: List[str] = ["*"]):
    """Add CORS middleware to the application."""
    
    if allow_origins is None:
        allow_origins = [
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:8000",
            "https://localhost",
            "https://localhost:3000",
            "https://localhost:8000",
        ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        # Allow credentials to be included in requests
        allow_origin_regex=r"https?://localhost(:[0-9]+)?",
    )