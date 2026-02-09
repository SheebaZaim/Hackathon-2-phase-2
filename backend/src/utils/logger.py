import logging
import sys
from pathlib import Path
from datetime import datetime

from ..config.settings import settings


def setup_logger(name: str, log_file: str = None, level: str = None):
    """
    Function to setup a logger with file and console handlers
    """
    if level is None:
        level = settings.log_level
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    # Prevent adding duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(settings.log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_path = log_dir / log_file
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Predefined loggers for common use cases
api_logger = setup_logger("api_logger", "api.log")
verification_logger = setup_logger("verification_logger", "verification.log")
error_logger = setup_logger("error_logger", "error.log", "ERROR")


def log_verification_event(event_type: str, component: str, status: str, details: str = ""):
    """
    Log a verification event with standardized format
    """
    verification_logger.info(
        f"VERIFICATION_EVENT - "
        f"Type: {event_type}, "
        f"Component: {component}, "
        f"Status: {status}, "
        f"Details: {details}"
    )


def log_error(error_message: str, error_type: str = "GENERAL"):
    """
    Log an error with standardized format
    """
    error_logger.error(
        f"ERROR - "
        f"Type: {error_type}, "
        f"Message: {error_message}, "
        f"Timestamp: {datetime.utcnow().isoformat()}"
    )