# Research: Teacher Planning App

## Overview
This research document addresses the requirements for transforming the existing Todo App into a secure multi-user full-stack web application for teachers to manage school plannings, upload or create student results, and handle task lists.

## Key Decisions Made

### 1. Technology Stack Selection
- **Decision**: Strictly adhere to the fixed technology stack defined in the constitution
- **Rationale**: The constitution mandates specific technologies (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT) which ensures consistency and compliance with project requirements.
- **Alternatives considered**: 
  - Alternative frameworks (React + Vite, Express.js, Sequelize): Rejected due to constitution requirements
  - Different databases (MongoDB, MySQL): Rejected due to constitution requirements
  - Different auth solutions (Auth0, Firebase Auth): Rejected due to constitution requirements

### 2. Authentication Architecture
- **Decision**: Implement Better Auth on the frontend with JWT token management
- **Rationale**: Better Auth provides a comprehensive authentication solution that works well with Next.js, and JWT tokens enable stateless authentication as required by the constitution.
- **Alternatives considered**:
  - Session-based authentication: Rejected as constitution requires stateless backend
  - Custom auth solution: Rejected as constitution specifies Better Auth + JWT

### 3. Data Isolation Strategy
- **Decision**: Implement user ID-based data partitioning in the backend with proper authorization checks
- **Rationale**: Each record will store the user ID, and all API endpoints will verify that the requesting user owns the data they're accessing. This ensures complete data isolation between users.
- **Alternatives considered**:
  - Separate databases per user: Too complex and not scalable
  - Row-level security: Possible but more complex than necessary for this implementation

### 4. Frontend Theming Approach
- **Decision**: Create a teacher-focused UI with school-themed colors (blues and greens) and education-oriented icons
- **Rationale**: The application needs to resonate with teachers and feel appropriate for educational planning tasks. Professional, clean design with intuitive organization will improve usability.
- **Alternatives considered**:
  - Generic todo app UI: Doesn't meet the teacher-focused requirement
  - Overly playful design: Might not feel professional enough for educators

### 5. Frontend Layout and Aesthetic Improvements
- **Decision**: Implement a balanced grid layout with properly sized elements and intuitive navigation
- **Rationale**: The existing application had layout issues with oversized centered images and elements pushed to extreme corners. The new design will feature a clean, professional interface with school-themed colors (blues and greens), properly sized and centered images that don't dominate the page, and a balanced grid layout avoiding extreme corner placements.
- **Alternatives considered**:
  - Keeping the existing layout: Would not meet the aesthetic improvement requirements
  - Minimalist design: Might lack the necessary visual cues for teachers

### 6. Authorization Button Enhancement
- **Decision**: Design prominent, intuitive login/register buttons with hover effects and include logout button in a persistent navbar
- **Rationale**: The authorization buttons need to be more user-friendly and accessible. This includes making them prominent with visual feedback on hover and ensuring logout functionality is always available.
- **Alternatives considered**:
  - Small, subtle buttons: Would not meet the usability requirements
  - Hidden behind menus: Would reduce accessibility

### 7. Editing Interface Design
- **Decision**: Create dedicated columns/modals for editing tasks/lists with fields for teacher-specific details
- **Rationale**: Teachers need specialized fields for educational contexts such as due dates for assignments, student names for results, and categories for school plannings like lesson plans or grading. The editing interface should be intuitive and include all necessary fields without clutter.
- **Alternatives considered**:
  - Generic editing fields: Would not meet the teacher-specific requirements
  - Complex multi-step forms: Would reduce usability

## Best Practices Applied

### Security Best Practices
- Implement proper JWT token validation and expiration handling
- Use parameterized queries to prevent SQL injection
- Implement proper input validation and sanitization
- Secure environment variables for sensitive data
- Implement proper error handling without exposing sensitive information

### Performance Best Practices
- Optimize database queries with proper indexing
- Implement caching for frequently accessed data
- Use pagination for large datasets
- Optimize frontend bundle size
- Implement proper loading states and error boundaries

### Code Quality Best Practices
- Follow consistent naming conventions
- Write comprehensive unit and integration tests
- Implement proper error handling and logging
- Use TypeScript for frontend type safety
- Follow Python best practices for backend code

## Implementation Patterns

### Backend API Pattern
```python
# Example of authenticated endpoint with user ownership validation
@router.get("/school-plannings/{planning_id}")
def get_school_planning(
    planning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    planning = session.get(SchoolPlanning, planning_id)
    if not planning or planning.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Planning not found")
    return planning
```

### Frontend Authentication Pattern
```javascript
// Example of JWT token handling in frontend service
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('better-auth-token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
```

### Database Model Pattern
```python
# Example of user-owned entity model
class SchoolPlanning(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default=None)
    subject: str
    grade_level: str
    date: datetime
    duration: int = Field(default=None)
    materials_needed: str = Field(default=None)
    learning_objectives: str = Field(default=None)
    user_id: int = Field(foreign_key="user.id")
    
    # Relationship to user
    user: User = Relationship(back_populates="school_plannings")
```