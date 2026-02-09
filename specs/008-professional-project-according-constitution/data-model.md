# Data Model: Professional Project According to Constitution

## Overview
This document defines the data model for the professional project according to the constitution. The model is designed to support a secure multi-user todo application with individual task lists, authentication, and data persistence.

## Entity: User
**Description**: Represents a registered user of the system with unique credentials, profile information, and access to their personal todo lists.

**Fields**:
- id: UUID (Primary Key)
- email: String (Unique, Required, Indexed)
- username: String (Unique, Required, Indexed)
- hashed_password: String (Required)
- first_name: String (Optional)
- last_name: String (Optional)
- is_active: Boolean (Default: True)
- created_at: DateTime (Auto-generated)
- updated_at: DateTime (Auto-generated)
- last_login_at: DateTime (Optional)

**Validation Rules**:
- Email must be a valid email format
- Username must be 3-30 characters, alphanumeric with underscores/hyphens
- Password must meet complexity requirements (8+ characters)
- Email and username must be unique across all users

**Relationships**:
- One-to-Many: User -> TodoList
- One-to-Many: User -> Task (through TodoList)

## Entity: TodoList
**Description**: A collection of tasks that belongs to a specific user, allowing for organization and categorization of tasks.

**Fields**:
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User.id, Required)
- title: String (Required, Max: 100 characters)
- description: Text (Optional, Max: 500 characters)
- is_public: Boolean (Default: False)
- created_at: DateTime (Auto-generated)
- updated_at: DateTime (Auto-generated)
- position: Integer (For ordering, Default: 0)

**Validation Rules**:
- Title must not be empty
- User must exist
- Only the owner can modify the list (unless public)

**Relationships**:
- Many-to-One: TodoList -> User
- One-to-Many: TodoList -> Task

## Entity: Task
**Description**: Individual items within a todo list that represent specific actions or goals, with properties like title, description, completion status, and due date.

**Fields**:
- id: UUID (Primary Key)
- todo_list_id: UUID (Foreign Key to TodoList.id, Required)
- title: String (Required, Max: 200 characters)
- description: Text (Optional)
- is_completed: Boolean (Default: False)
- priority: Enum (Values: low, medium, high, Default: medium)
- due_date: DateTime (Optional)
- created_at: DateTime (Auto-generated)
- updated_at: DateTime (Auto-generated)
- completed_at: DateTime (Optional)
- position: Integer (For ordering, Default: 0)

**Validation Rules**:
- Title must not be empty
- TodoList must exist and belong to the user
- Due date cannot be in the past (optional validation)

**Relationships**:
- Many-to-One: Task -> TodoList
- Many-to-One: Task -> User (through TodoList)

## Entity: AuthenticationToken
**Description**: JWT-based tokens that verify user identity and authorize access to system resources.

**Fields**:
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User.id, Required)
- token_hash: String (Required, Unique)
- token_type: Enum (Values: access, refresh, Default: access)
- expires_at: DateTime (Required)
- created_at: DateTime (Auto-generated)
- revoked_at: DateTime (Optional)

**Validation Rules**:
- Token hash must be unique
- Expiration date must be in the future
- Cannot be revoked before creation

**Relationships**:
- Many-to-One: AuthenticationToken -> User

## Indexes
- User.email: Unique index for fast lookup and validation
- User.username: Unique index for fast lookup and validation
- TodoList.user_id: Index for efficient user-specific queries
- Task.todo_list_id: Index for efficient list-specific queries
- Task.is_completed: Index for filtering completed tasks
- AuthenticationToken.token_hash: Unique index for fast token validation
- AuthenticationToken.expires_at: Index for token cleanup jobs

## Constraints
- Referential integrity: Foreign key constraints enforce relationships
- Data isolation: Users can only access their own data (enforced by application logic)
- Soft deletes: Consider implementing soft deletes for audit trails
- Archiving: Old inactive records may be archived to improve performance

## State Transitions
- Task: Pending -> Completed (when is_completed is set to true)
- AuthenticationToken: Active -> Revoked (when revoked_at is set)
- User: Active -> Inactive (when is_active is set to false)