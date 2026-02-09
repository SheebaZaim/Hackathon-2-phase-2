# Implementation Plan: Teacher Planning App

**Branch**: `005-teacher-planning-app` | **Date**: 2026-02-07 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/005-teacher-planning-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan transforms the existing Todo App into a secure multi-user full-stack web application specifically designed for teachers to manage school plannings, upload or create student results, and handle task lists. The implementation will leverage the fixed technology stack mandated by the constitution (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT) to create a teacher-focused application with proper authentication, data isolation, and role-based access controls. The plan addresses existing issues by enhancing frontend aesthetics with a modern teacher-friendly design, redesigning authorization buttons for better usability, adding intuitive editing interfaces with teacher-specific fields, and adapting Todo features for education with relevant icons and labels. The implementation ensures functional connectivity between frontend and backend via authenticated REST APIs with JWT token handling and data syncing with Neon PostgreSQL.

## Technical Context

**Language/Version**: JavaScript/TypeScript (Next.js 16+), Python 3.11+ (FastAPI)
**Primary Dependencies**: Next.js 16+ (App Router), FastAPI, SQLModel, Neon PostgreSQL, Better Auth, JWT
**Storage**: Neon Serverless PostgreSQL database
**Testing**: pytest for backend, Jest/React Testing Library for frontend, Playwright for E2E tests
**Target Platform**: Web application (cross-platform access)
**Project Type**: Web application (separate frontend/backend services)
**Performance Goals**: Pages load within 3 seconds, API responses under 500ms, support hundreds of concurrent users
**Constraints**: Must follow fixed technology stack, maintain service separation, implement stateless authentication
**Scale/Scope**: Multi-tenant SaaS application supporting multiple teachers with data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution, this implementation plan adheres to the following principles:

- **Library-First**: N/A - this is a full-stack application feature, not a library
- **CLI Interface**: N/A - this is a web application feature
- **Test-First**: YES - tests will be written for all critical functionality
- **Integration Testing**: YES - will include tests for frontend-backend communication, authentication flows, and data isolation
- **Observability**: YES - will include proper logging and error reporting for security and performance monitoring

**Constitution Compliance Verification**:
- ✅ Fixed Technology Stack: Using Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT
- ✅ Architecture Constraints: Frontend and backend remain as separate services
- ✅ Authentication & Security Rules: Implementing Better Auth + JWT with stateless backend
- ✅ Development Methodology: Following Spec-Driven Development with agentic workflow

All constitution gates pass for this feature implementation.

## Project Structure

### Documentation (this feature)

```text
specs/005-teacher-planning-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
For this teacher planning application:

```text
backend/
├── src/
│   ├── models/
│   │   ├── user_model.py
│   │   ├── school_planning_model.py
│   │   ├── student_result_model.py
│   │   └── task_model.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── school_planning_service.py
│   │   ├── student_result_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── auth_router.py
│   │   ├── school_planning_router.py
│   │   ├── student_result_router.py
│   │   └── task_router.py
│   ├── middleware/
│   │   └── jwt_middleware.py
│   └── main.py
├── requirements.txt
└── tests/
    ├── test_auth.py
    ├── test_school_planning.py
    ├── test_student_results.py
    └── test_tasks.py

frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.jsx
│   │   │   │   └── RegisterForm.jsx
│   │   │   ├── planning/
│   │   │   │   ├── PlanningList.jsx
│   │   │   │   └── PlanningForm.jsx
│   │   │   ├── results/
│   │   │   │   ├── ResultsList.jsx
│   │   │   │   └── ResultsForm.jsx
│   │   │   ├── tasks/
│   │   │   │   ├── TaskList.jsx
│   │   │   │   └── TaskForm.jsx
│   │   │   └── ui/
│   │   │       ├── Navbar.jsx
│   │   │       └── ProtectedRoute.jsx
│   │   ├── dashboard/
│   │   ├── login/
│   │   ├── register/
│   │   └── globals.css
│   ├── lib/
│   │   ├── auth.js
│   │   ├── api.js
│   │   └── utils.js
│   └── services/
│       ├── authService.js
│       ├── planningService.js
│       ├── resultsService.js
│       └── taskService.js
├── package.json
├── next.config.js
└── tests/
    ├── components/
    ├── pages/
    └── e2e/
        └── teacher-workflow.spec.js

config/
├── dev/
│   ├── backend.env
│   └── frontend.env
├── staging/
│   ├── backend.env
│   └── frontend.env
└── production/
    ├── backend.env
    └── frontend.env
```

**Structure Decision**: This is a full-stack teacher planning application with separate frontend and backend services as required by the constitution. The frontend uses Next.js 16+ with App Router for the teacher-focused UI, while the backend uses FastAPI with SQLModel for data management. The structure ensures proper separation of concerns while maintaining the required authentication and data isolation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
