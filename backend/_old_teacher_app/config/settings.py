from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    allowed_origins: List[str] = [
        "http://localhost:3000",  # Frontend development
        "http://localhost:8000",  # If serving frontend from same server
        # Add your production domain here
    ]

    # Database settings
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./todo_app.db"))

    # Auth settings
    auth_secret: str = Field(default_factory=lambda: os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_development"))

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()