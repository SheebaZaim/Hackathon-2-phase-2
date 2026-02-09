# API Contract: Teacher Planning Application

## Overview
This contract defines the API endpoints and behaviors for the teacher planning application. The API follows RESTful principles and uses JWT authentication for all protected endpoints.

## Authentication Contract

### Registration
- **Endpoint**: `POST /api/auth/register`
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required, min 8 chars)"
  }
  ```
- **Response**:
  ```json
  {
    "id": "UUID",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "created_at": "datetime"
  }
  ```
- **Authentication**: None required
- **Success Code**: 201 Created
- **Error Codes**: 400 Bad Request, 409 Conflict (email exists)

### Login
- **Endpoint**: `POST /api/auth/login`
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "JWT token string",
    "token_type": "bearer"
  }
  ```
- **Authentication**: None required
- **Success Code**: 200 OK
- **Error Codes**: 400 Bad Request, 401 Unauthorized

### Logout
- **Endpoint**: `POST /api/auth/logout`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Response**: Empty body
- **Authentication**: JWT Token required
- **Success Code**: 200 OK
- **Error Codes**: 401 Unauthorized

## School Planning Contract

### Get All Plannings
- **Endpoint**: `GET /api/plannings`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Response**:
  ```json
  [
    {
      "id": "UUID",
      "title": "string",
      "description": "string",
      "subject": "string",
      "grade_level": "string",
      "date": "datetime",
      "duration": "integer",
      "materials_needed": "string",
      "learning_objectives": "string",
      "class_size": "integer",
      "teaching_method": "string",
      "assessment_type": "string",
      "standards_addressed": "string",
      "previous_knowledge_required": "string",
      "extension_activities": "string",
      "differentiation_strategies": "string",
      "resources_links": "string",
      "user_id": "UUID",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
  ```
- **Authentication**: JWT Token required
- **Success Code**: 200 OK
- **Error Codes**: 401 Unauthorized

### Create Planning
- **Endpoint**: `POST /api/plannings`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "title": "string (required, 3-100 chars)",
    "description": "string",
    "subject": "string (required)",
    "grade_level": "string (required)",
    "date": "datetime (required)",
    "duration": "integer (optional)",
    "materials_needed": "string (optional)",
    "learning_objectives": "string (optional)",
    "class_size": "integer (optional)",
    "teaching_method": "string (optional)",
    "assessment_type": "string (optional)",
    "standards_addressed": "string (optional)",
    "previous_knowledge_required": "string (optional)",
    "extension_activities": "string (optional)",
    "differentiation_strategies": "string (optional)",
    "resources_links": "string (optional)"
  }
  ```
- **Response**: Created planning object
- **Authentication**: JWT Token required
- **Success Code**: 201 Created
- **Error Codes**: 400 Bad Request, 401 Unauthorized

### Get Specific Planning
- **Endpoint**: `GET /api/plannings/{id}`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Response**: Single planning object
- **Authentication**: JWT Token required
- **Success Code**: 200 OK
- **Error Codes**: 401 Unauthorized, 404 Not Found

### Update Planning
- **Endpoint**: `PUT /api/plannings/{id}`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Request Body**: Same as create but all fields optional
- **Response**: Updated planning object
- **Authentication**: JWT Token required
- **Success Code**: 200 OK
- **Error Codes**: 400 Bad Request, 401 Unauthorized, 404 Not Found

### Delete Planning
- **Endpoint**: `DELETE /api/plannings/{id}`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Response**: Empty body
- **Authentication**: JWT Token required
- **Success Code**: 204 No Content
- **Error Codes**: 401 Unauthorized, 404 Not Found

## Student Results Contract

### Get All Results
- **Endpoint**: `GET /api/results`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Response**: Array of student result objects
- **Authentication**: JWT Token required
- **Success Code**: 200 OK
- **Error Codes**: 401 Unauthorized

### Create Result
- **Endpoint**: `POST /api/results`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "student_name": "string (required)",
    "assignment_title": "string (required)",
    "score": "number (required)",
    "max_score": "number (required)",
    "subject": "string (required)",
    "date_recorded": "datetime (required)",
    "comments": "string (optional)"
  }
  ```
- **Response**: Created result object
- **Authentication**: JWT Token required
- **Success Code**: 201 Created
- **Error Codes**: 400 Bad Request, 401 Unauthorized

## Tasks Contract

### Get All Tasks
- **Endpoint**: `GET /api/tasks`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Response**: Array of task objects
- **Authentication**: JWT Token required
- **Success Code**: 200 OK
- **Error Codes**: 401 Unauthorized

### Create Task
- **Endpoint**: `POST /api/tasks`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Request Body**:
  ```json
  {
    "title": "string (required, 3-100 chars)",
    "description": "string (optional)",
    "due_date": "datetime (required)",
    "category": "string (required, e.g., lesson planning, grading, meeting, parent conference)",
    "priority": "string (optional, default: medium, values: low, medium, high)",
    "assigned_class": "string (optional)",
    "subject_area": "string (optional)",
    "estimated_time": "integer (optional, minutes)",
    "related_planning_id": "integer (optional, foreign key to school planning)",
    "students_involved": "string (optional, comma-separated list)",
    "recurring": "boolean (optional, default: false)",
    "recurring_frequency": "string (optional, values: daily, weekly, monthly)",
    "reminders_enabled": "boolean (optional, default: false)",
    "remind_before": "integer (optional, minutes before due date)"
  }
  ```
- **Response**: Created task object
- **Authentication**: JWT Token required
- **Success Code**: 201 Created
- **Error Codes**: 400 Bad Request, 401 Unauthorized

### Toggle Task Completion
- **Endpoint**: `PATCH /api/tasks/{id}/toggle`
- **Request Headers**: 
  - `Authorization: Bearer {token}`
- **Response**: Updated task object
- **Authentication**: JWT Token required
- **Success Code**: 200 OK
- **Error Codes**: 401 Unauthorized, 404 Not Found

## Data Isolation Contract
- All endpoints that return user-specific data will only return records owned by the authenticated user
- Attempts to access another user's data will result in 404 Not Found
- All create endpoints will automatically associate the new record with the authenticated user
- The user_id field is populated server-side and cannot be overridden by the client

## Error Response Format
All error responses follow this format:
```json
{
  "detail": "Human-readable error message"
}
```

## Rate Limiting
- API endpoints are rate-limited to prevent abuse
- Excessive requests will result in 429 Too Many Requests response
- Limits are set appropriately for normal usage patterns