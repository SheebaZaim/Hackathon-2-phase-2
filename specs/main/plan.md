# Implementation Plan: Todo App Phase II

**Branch**: `1-todo-spec` | **Date**: 2026-01-26 | **Spec**: [sp.specify.md](./sp.specify.md)
**Input**: Feature specification from `/specs/sp.specify.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a secure multi-user todo web application with JWT-based authentication. The system transforms a console app into a full-stack web application with Next.js frontend, FastAPI backend, SQLModel ORM, and Neon PostgreSQL database. The architecture enforces strict user data isolation with Better Auth handling frontend authentication and JWT tokens for backend API communication.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript (Next.js 16+)
**Primary Dependencies**: FastAPI, SQLModel, Next.js, Better Auth, Neon PostgreSQL driver
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest, Jest
**Target Platform**: Web application (Linux/Mac/Windows compatible)
**Project Type**: Web (full-stack with separate frontend and backend services)
**Performance Goals**: 100 concurrent users, <2 second response times
**Constraints**: JWT stateless authentication, user data isolation, 99.9% uptime
**Scale/Scope**: Multi-user support, persistent storage, secure authentication

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Technology Stack Compliance**: All components align with fixed stack (Next.js 16+, Python FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT)
2. **Architecture Constraints**: Frontend and backend remain as separate services with no tight coupling
3. **Authentication Compliance**: Better Auth runs only on frontend, JWT used for backend communication with shared secret verification
4. **Security Requirements**: All sensitive data encrypted at rest and in transit, stateless session management with proper token expiration

## Project Structure

### Documentation (this feature)

```text
specs/
├── sp.plan.md             # This file (/sp.plan command output)
├── sp.specify.md          # Feature specification
└── checklists/
    └── requirements.md    # Quality checklist
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── task_model.py    # SQLModel definitions
│   ├── services/
│   │   ├── auth_service.py  # JWT verification logic
│   │   └── task_service.py  # Task CRUD operations
│   ├── api/
│   │   ├── auth_router.py   # Authentication endpoints
│   │   ├── task_router.py   # Task management endpoints
│   │   └── user_router.py   # User profile endpoints
│   ├── middleware/
│   │   └── jwt_middleware.py # Authentication middleware
│   └── main.py              # FastAPI application entry point
├── requirements.txt         # Python dependencies
└── tests/
    ├── unit/
    └── integration/

frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth_api.js    # Authentication API calls
│   │   │   └── task_api.js    # Task API calls
│   │   ├── components/
│   │   │   ├── TaskList.jsx   # Task list component
│   │   │   ├── TaskForm.jsx   # Task creation/editing form
│   │   │   └── AuthComponents.jsx # Login/Register components
│   │   ├── pages/
│   │   │   ├── login/page.jsx
│   │   │   ├── register/page.jsx
│   │   │   ├── dashboard/page.jsx
│   │   │   └── profile/page.jsx
│   │   └── layout.jsx         # Main layout
│   ├── lib/
│   │   └── auth.js            # Better Auth configuration
│   └── styles/
└── package.json             # Node.js dependencies

.history/
└── prompts/
    └── spec/
        └── todo-app-phase-ii-specification.prompt.md # PHR for spec
```

**Structure Decision**: Selected Option 2: Web application with separate backend and frontend services to maintain loose coupling as required by architecture constraints. Backend uses Python FastAPI with SQLModel, while frontend uses Next.js 16+ with Better Auth for authentication management.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |

## Planning Overview

This plan outlines the step-by-step implementation of the Phase II Todo Full-Stack Web Application. The approach follows spec-driven execution, ensuring all development activities align with the established constitution and feature specification. The implementation will proceed through 8 distinct phases, each building upon the previous phase to create a complete, secure, and functional application.

## Phase 1: Monorepo & Environment Setup

1. **Folder structure creation**:
   - Create `backend/` directory with proper Python project structure
   - Create `frontend/` directory with Next.js project structure
   - Establish configuration files for both services

2. **Spec-Kit configuration**:
   - Initialize proper configuration for multi-service monorepo
   - Set up shared environment management
   - Configure linting and formatting standards

3. **Environment variables setup**:
   - Define `BETTER_AUTH_SECRET` for JWT signing
   - Configure Neon PostgreSQL connection strings
   - Set up CORS and other security configurations

## Phase 2: Database Layer

1. **SQLModel schema definition**:
   - Create Task model with fields: id, title, description, completed, timestamps, user_id
   - Define relationships and constraints
   - Implement validation rules

2. **Neon PostgreSQL connection**:
   - Set up connection pooling
   - Configure SSL and security settings
   - Implement database initialization scripts

3. **Persistent storage setup**:
   - Create migration system
   - Set up database seeding for development
   - Implement backup and recovery procedures

## Phase 3: Backend Authentication

1. **JWT middleware creation**:
   - Develop middleware to intercept and validate JWT tokens
   - Extract user identity from token claims
   - Handle token expiration and invalidation

2. **Token extraction and verification**:
   - Implement JWT parsing from Authorization header
   - Verify signature using shared secret
   - Validate token expiration and audience

3. **User identity extraction**:
   - Extract user_id, email from JWT claims
   - Create user context for request handlers
   - Log authentication events for security

4. **Error handling (401/403)**:
   - Return appropriate HTTP status codes
   - Implement consistent error response format
   - Add security logging for unauthorized access attempts

## Phase 4: Backend API Implementation

1. **CRUD endpoints**:
   - Implement GET /api/tasks for retrieving user's tasks
   - Implement POST /api/tasks for creating new tasks
   - Implement PUT /api/tasks/{id} for updating tasks
   - Implement DELETE /api/tasks/{id} for deleting tasks

2. **Ownership enforcement**:
   - Validate that users can only access their own tasks
   - Implement database-level filtering based on user_id
   - Prevent cross-user data access

3. **Completion toggle logic**:
   - Implement PUT endpoint to toggle task completion status
   - Update timestamps appropriately
   - Validate ownership before allowing updates

## Phase 5: Frontend Authentication

1. **Better Auth setup**:
   - Install and configure Better Auth library
   - Set up authentication pages (login, register)
   - Configure session management

2. **JWT plugin enablement**:
   - Enable JWT token handling in Better Auth
   - Configure token refresh mechanisms
   - Set up proper token storage and retrieval

3. **Secure token handling**:
   - Implement secure storage of JWT tokens
   - Handle token expiration gracefully
   - Add automatic token refresh logic

## Phase 6: Frontend UI

1. **Task list UI**:
   - Create responsive task list component
   - Implement task display with completion status
   - Add sorting and filtering capabilities

2. **Task create/update UI**:
   - Design intuitive task creation form
   - Implement inline editing capabilities
   - Add validation and error handling

3. **Auth-protected routes**:
   - Implement route guards for protected pages
   - Redirect unauthenticated users appropriately
   - Handle session expiration

4. **Responsive design**:
   - Ensure mobile-friendly interface
   - Optimize for different screen sizes
   - Implement accessibility features

## Phase 7: Integration & Validation

1. **End-to-end auth testing**:
   - Test complete authentication flow
   - Verify JWT token handling end-to-end
   - Validate secure session management

2. **Multi-user isolation verification**:
   - Test data isolation between users
   - Verify that users cannot access others' tasks
   - Confirm ownership enforcement at all levels

3. **API security validation**:
   - Test all security measures are functioning
   - Validate error handling and responses
   - Verify proper authentication on all protected endpoints

## Phase 8: Documentation & Cleanup

1. **README documentation**:
   - Create comprehensive project documentation
   - Include setup and deployment instructions
   - Document API endpoints and usage

2. **Environment setup guides**:
   - Provide detailed environment configuration
   - Document required environment variables
   - Include troubleshooting guidelines