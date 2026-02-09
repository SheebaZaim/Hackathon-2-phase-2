# Data Model: Project Cleanup and Functional Setup

**Feature**: 001-cleanup-functional-project
**Date**: 2026-02-09
**Status**: Complete

## Overview

This document defines the data entities for the multi-user todo application. The model is kept simple and focused on core functionality: user management and task management.

## Entity Relationship Diagram

```
┌─────────────┐         ┌─────────────┐
│    User     │1      N │    Task     │
│─────────────│◄────────┤─────────────│
│ id          │         │ id          │
│ email       │         │ user_id (FK)│
│ password... │         │ title       │
│ created_at  │         │ description │
│ updated_at  │         │ completed   │
└─────────────┘         │ created_at  │
                        │ updated_at  │
                        └─────────────┘
```

## Entities

### 1. User

**Purpose**: Represents a registered user of the application. Each user has their own isolated set of tasks.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, AUTO | Unique identifier for the user |
| email | String(255) | UNIQUE, NOT NULL | User's email address (used for login) |
| password_hash | String(255) | NOT NULL | Bcrypt hashed password |
| created_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when user was created |
| updated_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when user was last updated |

**Validation Rules**:
- Email must be valid format (regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
- Email must be unique (enforced at database level)
- Password must be at least 8 characters before hashing
- Password must contain at least: 1 uppercase, 1 lowercase, 1 number
- Password is never stored in plain text (always hashed with bcrypt)

**Indexes**:
- Primary index on `id` (automatic)
- Unique index on `email` for fast lookups during login
- Index on `created_at` for sorting users by registration date

**Relationships**:
- One User has many Tasks (1:N relationship)

**State Transitions**: None (users don't have status states in this simple implementation)

### 2. Task

**Purpose**: Represents a single todo task belonging to a user. Tasks can be created, updated, completed, and deleted.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, AUTO | Unique identifier for the task |
| user_id | UUID | FOREIGN KEY, NOT NULL | References User.id (owner of the task) |
| title | String(255) | NOT NULL | Short title/summary of the task |
| description | Text | NULLABLE | Detailed description of the task |
| completed | Boolean | NOT NULL, DEFAULT FALSE | Whether the task is completed |
| created_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when task was created |
| updated_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when task was last updated |

**Validation Rules**:
- Title must not be empty (minimum 1 character)
- Title maximum length is 255 characters
- Description is optional but if provided, maximum 10,000 characters
- user_id must reference an existing user
- completed defaults to false for new tasks

**Indexes**:
- Primary index on `id` (automatic)
- Index on `user_id` for fast filtering of tasks by user
- Composite index on `(user_id, completed)` for filtering completed/incomplete tasks per user
- Index on `created_at` for sorting tasks by creation date

**Relationships**:
- Each Task belongs to one User (N:1 relationship)
- ON DELETE CASCADE: If a user is deleted, all their tasks are deleted

**State Transitions**:
```
[ ] Incomplete ──(mark complete)──> [x] Complete
[x] Complete ──(mark incomplete)──> [ ] Incomplete
```

## Business Rules

### Data Isolation
- Users can only access their own tasks
- All task queries must include user_id filter
- Backend API must verify user ownership before allowing updates/deletes

### Audit Trail
- `created_at` is set once on creation and never modified
- `updated_at` is automatically updated on every modification
- These timestamps provide basic audit capability

### Soft Delete (Out of Scope)
- Hard delete is used for simplicity
- Soft delete (deleted_at field) is out of scope for this feature

### Cascading Deletes
- When a user is deleted, all associated tasks are automatically deleted
- This prevents orphaned tasks in the database

## Data Constraints

### Performance Constraints
- Task queries should return in <100ms for up to 1,000 tasks per user
- User lookups by email should return in <50ms

### Scalability Constraints
- System should support up to 10,000 users
- Each user can have up to 10,000 tasks
- Total database size estimated at <1GB for initial deployment

### Security Constraints
- Passwords are never stored in plain text
- User emails are considered PII and must be encrypted at rest (handled by Neon)
- Task data is isolated per user (enforced at application level)

## Schema Migration Notes

### Initial Schema Creation
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

### Trigger for updated_at
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

## SQLModel Implementation Notes

These entities will be implemented in SQLModel with the following patterns:

- Use `Field(primary_key=True, default_factory=uuid.uuid4)` for UUID primary keys
- Use `Field(foreign_key="users.id")` for relationships
- Use `Field(sa_column_kwargs={"onupdate": datetime.utcnow})` for updated_at
- Use Pydantic validators for email format and password strength
- Separate base models (SQLModel) from API models (Pydantic)

Example structure:
```python
# models/user.py
from sqlmodel import Field, SQLModel
from typing import Optional
import uuid
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## API Data Transfer Objects (DTOs)

Separate from database models, the API will use these DTOs:

### Request DTOs
- `UserCreateRequest`: { email, password }
- `TaskCreateRequest`: { title, description? }
- `TaskUpdateRequest`: { title?, description?, completed? }

### Response DTOs
- `UserResponse`: { id, email, created_at } (no password_hash)
- `TaskResponse`: { id, title, description, completed, created_at, updated_at }

## Future Enhancements (Out of Scope)

These are potential enhancements but are explicitly out of scope for this feature:

- Task categories/tags
- Task priorities
- Due dates
- Task assignments (sharing tasks)
- Task attachments
- Task comments
- Activity logs
- Soft delete with deleted_at field
- Full-text search on task titles/descriptions
