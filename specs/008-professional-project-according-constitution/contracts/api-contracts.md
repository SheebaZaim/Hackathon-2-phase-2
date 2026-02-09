# API Contracts: Professional Project According to Constitution

## Overview
This document defines the API contracts for the professional project according to the constitution. The API follows RESTful patterns with proper error handling as required by the constitution.

## Authentication Endpoints

### POST /auth/register
Register a new user account
- **Request Body**: 
  ```json
  {
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securePassword123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- **Response 201**: 
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Response 400**: Validation error
- **Response 409**: User already exists

### POST /auth/login
Authenticate user and return JWT token
- **Request Body**: 
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Response 200**: 
  ```json
  {
    "access_token": "jwt-token-string",
    "token_type": "bearer",
    "expires_in": 3600
  }
  ```
- **Response 401**: Invalid credentials

### POST /auth/logout
Logout user and invalidate token
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 200**: 
  ```json
  {
    "message": "Successfully logged out"
  }
  ```

## User Endpoints

### GET /users/me
Get current user's profile
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 200**: 
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```

### PUT /users/me
Update current user's profile
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Request Body**: 
  ```json
  {
    "first_name": "Jane",
    "last_name": "Smith"
  }
  ```
- **Response 200**: Updated user object

## Todo List Endpoints

### GET /todo-lists
Get all todo lists for the current user
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 200**: 
  ```json
  [
    {
      "id": "uuid-string",
      "user_id": "uuid-string",
      "title": "Work Tasks",
      "description": "Tasks for work",
      "is_public": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "position": 0
    }
  ]
  ```

### POST /todo-lists
Create a new todo list
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Request Body**: 
  ```json
  {
    "title": "Personal Tasks",
    "description": "My personal tasks",
    "is_public": false
  }
  ```
- **Response 201**: Created todo list object

### GET /todo-lists/{id}
Get a specific todo list
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 200**: Todo list object

### PUT /todo-lists/{id}
Update a specific todo list
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Request Body**: 
  ```json
  {
    "title": "Updated Title",
    "description": "Updated description",
    "is_public": true
  }
  ```
- **Response 200**: Updated todo list object

### DELETE /todo-lists/{id}
Delete a specific todo list
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 204**: No content

## Task Endpoints

### GET /todo-lists/{todo_list_id}/tasks
Get all tasks for a specific todo list
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 200**: 
  ```json
  [
    {
      "id": "uuid-string",
      "todo_list_id": "uuid-string",
      "title": "Complete project",
      "description": "Finish the project by deadline",
      "is_completed": false,
      "priority": "high",
      "due_date": "2023-12-31T23:59:59Z",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "completed_at": null,
      "position": 0
    }
  ]
  ```

### POST /todo-lists/{todo_list_id}/tasks
Create a new task in a specific todo list
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Request Body**: 
  ```json
  {
    "title": "New Task",
    "description": "Task description",
    "priority": "medium",
    "due_date": "2023-12-31T23:59:59Z"
  }
  ```
- **Response 201**: Created task object

### GET /tasks/{id}
Get a specific task
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 200**: Task object

### PUT /tasks/{id}
Update a specific task
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Request Body**: 
  ```json
  {
    "title": "Updated Task",
    "description": "Updated description",
    "is_completed": true,
    "priority": "low",
    "due_date": "2023-12-31T23:59:59Z"
  }
  ```
- **Response 200**: Updated task object

### PATCH /tasks/{id}/toggle-completion
Toggle completion status of a specific task
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 200**: Updated task object

### DELETE /tasks/{id}
Delete a specific task
- **Headers**: 
  ```
  Authorization: Bearer {access_token}
  ```
- **Response 204**: No content

## Error Response Format
All error responses follow this format:
```json
{
  "detail": "Human-readable error message",
  "error_code": "machine-readable-error-code",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Common HTTP Status Codes
- 200: OK - Request successful
- 201: Created - Resource created successfully
- 204: No Content - Request successful, no content to return
- 400: Bad Request - Client sent invalid request
- 401: Unauthorized - Authentication required
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource does not exist
- 409: Conflict - Resource already exists
- 500: Internal Server Error - Server error occurred