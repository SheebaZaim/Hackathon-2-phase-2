# Data Model: Todo App Phase II

## Task Entity

### Fields
- **id**: UUID/GUID, Primary Key, Auto-generated
- **title**: String, Required, Max length 255 characters
- **description**: String, Optional, Max length 1000 characters
- **completed**: Boolean, Default False
- **created_at**: DateTime, Auto-populated on creation
- **updated_at**: DateTime, Auto-populated on update
- **user_id**: UUID/GUID, Foreign Key to User table

### Relationships
- **Owner**: One-to-Many relationship with User entity
  - One User can own many Tasks
  - Each Task belongs to exactly one User
  - Cascade delete: Tasks deleted when User is deleted

### Validation Rules
- Title must not be empty
- Title must be between 1-255 characters
- Description must be between 0-1000 characters if provided
- Completed status must be boolean
- User_id must reference an existing User

## User Entity

### Fields
- **id**: UUID/GUID, Primary Key, Auto-generated
- **email**: String, Required, Unique, Max length 255 characters
- **password_hash**: String, Required, Encrypted password
- **created_at**: DateTime, Auto-populated on creation
- **updated_at**: DateTime, Auto-populated on update

### Validation Rules
- Email must be valid email format
- Email must be unique across all users
- Password must be properly hashed
- Email must be between 5-255 characters

## Access Control Rules

### Ownership Enforcement
- Users can only create, read, update, and delete their own tasks
- Users cannot access tasks owned by other users
- Backend enforces ownership checks on all operations
- Data filtering occurs at the database query level
- Administrative access to other users' tasks is prohibited