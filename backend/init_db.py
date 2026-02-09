#!/usr/bin/env python
"""
Database initialization script for the Todo App backend
"""

import os
import sys
# Add the current directory to the path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel, create_engine
from src.db import DATABASE_URL
from src.models.user_model import User
from src.models.task_model import Task

def init_db():
    """Initialize the database and create tables"""
    print("Initializing database...")

    # Create engine
    engine = create_engine(DATABASE_URL)

    # Create all tables
    print("Creating tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Tables created successfully!")

    return engine

if __name__ == "__main__":
    init_db()
    print("Database initialization completed.")