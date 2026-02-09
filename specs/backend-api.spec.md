# Teachers Planning App - Backend API Specification

## Architecture
- FastAPI backend with RESTful endpoints
- Stateful authentication via JWT tokens
- Neon PostgreSQL database
- SQLModel for ORM operations

## Authentication Requirements
- JWT required on every protected endpoint
- Stateless backend design
- Proper error responses with HTTP status codes
- Authorization header format: `Authorization: Bearer <token>`

## Base URL
- Production: `/api/v1/`
- Local development: `http://localhost:8000/api/v1/`

## Endpoints

### Authentication
- `POST /auth/login` - Authenticate teacher and return JWT
- `POST /auth/logout` - Invalidate current session
- `GET /auth/me` - Get current authenticated teacher info

### Classes
- `GET /classes` - Get all classes for current teacher
- `POST /classes` - Create a new class
- `GET /classes/{class_id}` - Get specific class details
- `PUT /classes/{class_id}` - Update class information
- `DELETE /classes/{class_id}` - Delete a class

### Students
- `GET /classes/{class_id}/students` - Get all students in a class
- `POST /classes/{class_id}/students` - Add a student to a class
- `GET /students/{student_id}` - Get specific student details
- `PUT /students/{student_id}` - Update student information
- `DELETE /students/{student_id}` - Remove student from class

### Subjects
- `GET /subjects` - Get all subjects for current teacher
- `POST /subjects` - Create a new subject
- `GET /subjects/{subject_id}` - Get specific subject details
- `PUT /subjects/{subject_id}` - Update subject information
- `DELETE /subjects/{subject_id}` - Delete a subject

### Results
- `GET /students/{student_id}/results` - Get all results for a student
- `POST /students/{student_id}/results` - Add a new result for a student
- `GET /results/{result_id}` - Get specific result details
- `PUT /results/{result_id}` - Update result information
- `DELETE /results/{result_id}` - Delete a result

## Request/Response Formats

### Common Response Structure
```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

### Error Response Structure
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Descriptive error message"
  }
}
```

## HTTP Status Codes
- `200 OK` - Successful GET, PUT requests
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Data Validation
- All inputs must be validated
- Proper error messages for validation failures
- Sanitization of user inputs to prevent injection attacks

## Security Measures
- Rate limiting on authentication endpoints
- Input sanitization to prevent XSS
- SQL injection prevention through ORM usage
- Proper JWT token validation and expiration