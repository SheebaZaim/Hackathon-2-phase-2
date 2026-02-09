# Implementation Plan: Project Cleanup and Functional Setup

**Branch**: `001-cleanup-functional-project` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cleanup-functional-project/spec.md`

## Summary

This feature cleans up the project structure and ensures all essential files are present and functional according to the constitution requirements. The primary goals are:

1. Remove unnecessary files and directories (test scripts, temp files, extra envs)
2. Ensure frontend (Next.js 16+ with Better Auth) and backend (FastAPI with SQLModel) are functional
3. Provide clear documentation and configuration examples
4. Establish a clean foundation following the constitution's fixed technology stack

**Technical Approach**: File system cleanup followed by validation of essential files, then functional testing of both frontend and backend services to ensure they meet constitution requirements.

## Technical Context

**Language/Version**:
- Frontend: JavaScript/TypeScript (Node.js 18+, Next.js 16+)
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16+, Better Auth, React, TailwindCSS (for responsive UI)
- Backend: FastAPI, SQLModel, psycopg2 (PostgreSQL driver), python-jose (JWT), passlib (password hashing)

**Storage**: Neon Serverless PostgreSQL (cloud-hosted)

**Testing**:
- Frontend: Manual testing (running dev server and verifying UI)
- Backend: Manual testing (health check endpoint, database connection)
- Note: Automated testing setup is out of scope per spec

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge)
- Backend: Linux/Windows server (local dev or cloud deployment)

**Project Type**: Web application (frontend + backend as separate services)

**Performance Goals**:
- Frontend startup: <5 seconds to display UI
- Backend startup: <2 seconds to respond to health check
- Database connection: <3 seconds to establish
- Developer setup: <10 minutes following README

**Constraints**:
- Must follow fixed technology stack (no deviations)
- Backend must be stateless (JWT only, no server-side sessions)
- Frontend and backend must be separate services (no monolith)
- All configuration via environment variables

**Scale/Scope**:
- Single developer environment setup
- Support for multiple users (multi-tenant with user isolation)
- Basic CRUD operations for todo tasks
- Authentication and authorization flows

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Technology Stack Compliance**:
- [x] Frontend: Next.js 16+ (App Router) - VERIFIED (per spec FR-005, FR-013)
- [x] Backend: Python FastAPI - VERIFIED (per spec FR-006, FR-013)
- [x] ORM: SQLModel - VERIFIED (per spec FR-006, FR-013)
- [x] Database: Neon Serverless PostgreSQL - VERIFIED (per spec FR-006, FR-013, Dependencies)
- [x] Authentication: Better Auth + JWT - VERIFIED (per spec FR-008, FR-013)

**Architecture Constraints**:
- [x] Frontend and backend as separate services - VERIFIED (per spec FR-014)
- [x] Stateless backend for authentication - VERIFIED (per spec FR-011)
- [x] JWT as only authentication mechanism between services - VERIFIED (per spec FR-008)
- [x] RESTful APIs with proper error handling - VERIFIED (per spec FR-012)

**Security Rules**:
- [x] Better Auth on frontend only - VERIFIED (per spec FR-008)
- [x] JWT tokens with secure storage - VERIFIED (per spec FR-008, Key Entities)
- [x] Authorization header for authenticated requests - VERIFIED (per spec FR-008)
- [x] Shared secret verification via BETTER_AUTH_SECRET - VERIFIED (per spec Key Entities)
- [x] Encryption at rest and in transit - VERIFIED (per spec Assumptions)
- [x] Stateless session management - VERIFIED (per spec FR-011)

**Constitution Compliance**: ✅ PASSED - All requirements aligned with constitution

## Project Structure

### Documentation (this feature)

```text
specs/001-cleanup-functional-project/
├── spec.md                          # Feature specification
├── plan.md                          # This file (/sp.plan command output)
├── research.md                      # Phase 0 output - technology research
├── data-model.md                    # Phase 1 output - database schema
├── quickstart.md                    # Phase 1 output - developer setup guide
├── contracts/                       # Phase 1 output - API contracts
│   ├── api-endpoints.yaml          # OpenAPI spec for backend
│   └── auth-flow.md                # Authentication flow documentation
└── checklists/
    └── requirements.md              # Specification quality checklist (completed)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend separate)
frontend/
├── src/
│   ├── app/                        # Next.js App Router pages
│   │   ├── page.tsx               # Homepage (auth or dashboard)
│   │   ├── auth/                  # Authentication pages
│   │   │   ├── signin/
│   │   │   └── signup/
│   │   └── dashboard/             # Protected dashboard
│   │       └── page.tsx           # Main todo interface
│   ├── components/                 # React components
│   │   ├── auth/                  # Auth-related components
│   │   ├── tasks/                 # Task management components
│   │   └── ui/                    # UI primitives
│   ├── lib/                       # Utility libraries
│   │   ├── auth.ts                # Better Auth configuration
│   │   ├── api-client.ts          # Backend API client
│   │   └── types.ts               # TypeScript types
│   └── styles/
│       └── globals.css            # TailwindCSS styles
├── public/                         # Static assets
├── .env.example                    # Environment variables template
├── package.json                    # Dependencies
├── next.config.js                  # Next.js configuration
└── tsconfig.json                   # TypeScript configuration

backend/
├── src/
│   ├── main.py                    # FastAPI application entry
│   ├── models/                    # SQLModel database models
│   │   ├── user.py               # User model
│   │   └── task.py               # Task model
│   ├── services/                  # Business logic
│   │   ├── auth.py               # JWT verification
│   │   └── tasks.py              # Task CRUD operations
│   ├── api/                       # API routes
│   │   ├── health.py             # Health check endpoint
│   │   ├── auth.py               # Auth verification endpoints
│   │   └── tasks.py              # Task CRUD endpoints
│   ├── middleware/                # Middleware
│   │   └── auth.py               # JWT authentication middleware
│   └── database/                  # Database configuration
│       └── connection.py          # Neon PostgreSQL connection
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
└── README.md                       # Backend-specific docs

# Root level (minimal files only)
.gitignore                          # Git ignore patterns
README.md                           # Project overview and setup
CLAUDE.md                           # Project instructions for Claude
package.json                        # Workspace scripts (optional)

# Keep existing (no changes)
specs/                              # Specification directory
.specify/                           # Spec-kit tools
.spec-kit/                          # Spec-kit configuration
.claude/                            # Claude configuration
history/                            # Prompt history records
```

**Structure Decision**: Web application (Option 2) is selected because the feature explicitly requires functional frontend and backend as separate services per constitution. The structure supports:
- Clear separation between frontend (Next.js) and backend (FastAPI)
- No tight coupling (separate package.json/requirements.txt, separate .env files)
- Independent deployment capability
- Constitution-compliant architecture

## Complexity Tracking

> **No violations detected** - All requirements align with constitution. No complexity justification needed.

## Phase 0: Research

**Objective**: Research best practices and resolve any technical uncertainties for implementing the cleanup and functional setup.

### Research Tasks

1. **Better Auth Integration with Next.js 16+**
   - Research: How to configure Better Auth in Next.js App Router
   - Research: JWT token generation and secure storage patterns
   - Research: Environment variable configuration for BETTER_AUTH_SECRET
   - Output: Configuration patterns and example code

2. **FastAPI JWT Verification**
   - Research: How to verify JWT tokens in FastAPI middleware
   - Research: python-jose library usage for JWT validation
   - Research: Stateless authentication patterns
   - Output: Middleware implementation pattern

3. **Neon PostgreSQL Connection with SQLModel**
   - Research: Neon connection string format and configuration
   - Research: SQLModel async/sync database patterns
   - Research: Connection pooling and error handling
   - Output: Database connection setup pattern

4. **Next.js + FastAPI Communication**
   - Research: CORS configuration for separate frontend/backend
   - Research: API client patterns (fetch/axios in Next.js)
   - Research: Error handling and response standardization
   - Output: API communication pattern

5. **Responsive UI Best Practices**
   - Research: TailwindCSS responsive design patterns
   - Research: Mobile-first vs desktop-first approach
   - Research: Simple and attractive UI component libraries
   - Output: UI design guidelines

**Output**: `research.md` documenting all findings, decisions, and code patterns

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete

### 1. Data Model Design

**Input**: Key Entities from spec (User, Task, Configuration)

**Tasks**:
- Design User entity (id, email, password_hash, created_at, updated_at)
- Design Task entity (id, user_id, title, description, completed, created_at, updated_at)
- Define relationships (User 1:N Task)
- Document validation rules (email format, password strength, task title required)
- Define indexes (user_id for tasks, email for users)

**Output**: `data-model.md` with SQLModel-agnostic entity definitions

### 2. API Contracts

**Input**: Functional requirements (FR-008, FR-012) and user stories

**Tasks**:
- Define authentication endpoints (verify JWT)
- Define task CRUD endpoints (GET /tasks, POST /tasks, PUT /tasks/:id, DELETE /tasks/:id)
- Define health check endpoint (GET /health)
- Document request/response schemas
- Document error responses
- Define authentication headers

**Output**: `contracts/api-endpoints.yaml` (OpenAPI 3.0 spec) and `contracts/auth-flow.md`

### 3. Quickstart Guide

**Input**: Success Criteria SC-009 (setup in <10 minutes)

**Tasks**:
- Document prerequisites (Node.js 18+, Python 3.11+, Neon account)
- Write step-by-step setup instructions
- Document environment variable configuration
- Provide example .env values
- Include troubleshooting section
- Add verification steps

**Output**: `quickstart.md`

### 4. Agent Context Update

**Task**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Expected Updates**: Add any new technology decisions from research.md to Claude's context

**Output**: Updated `.claude/` context files

## Implementation Phases (for /sp.tasks)

*Note: These phases will be converted to tasks by the `/sp.tasks` command*

### Phase A: Project Cleanup (Priority P1)

**Goal**: Remove all unnecessary files and directories

**Key Activities**:
1. Delete test scripts from root (check_neon_connection.py, create_tables_directly.py, etc.)
2. Delete summary markdown files (BACKEND_IMPLEMENTATION_SUMMARY.md, etc.)
3. Remove unnecessary directories (backend_env, backend_env_py311, -p, config, docs, tests, tasks, public, node_modules from root)
4. Verify only essential root files remain (CLAUDE.md, README.md, .gitignore, package.json)

**Verification**: Count files in root directory (should be <10 excluding hidden dirs)

### Phase B: Essential Files Setup (Priority P2)

**Goal**: Ensure all required files exist and are properly configured

**Key Activities**:
1. Create/update frontend/.env.example with documented variables
2. Create/update backend/.env.example with documented variables
3. Verify frontend/package.json has required dependencies
4. Verify backend/requirements.txt has required dependencies
5. Create/update README.md with setup instructions
6. Verify specs/overview.md exists

**Verification**: Check for presence of all .env.example files and documentation

### Phase C: Frontend Functionality (Priority P3)

**Goal**: Ensure frontend is functional with Better Auth

**Key Activities**:
1. Verify Next.js 16+ configuration
2. Implement Better Auth setup
3. Create authentication UI components (simple and attractive)
4. Implement responsive design with TailwindCSS
5. Create API client for backend communication
6. Test frontend startup and UI display

**Verification**: Run `npm run dev` and verify UI loads within 5 seconds

### Phase D: Backend Functionality (Priority P4)

**Goal**: Ensure backend is functional with FastAPI and Neon

**Key Activities**:
1. Verify FastAPI application setup
2. Implement database connection to Neon PostgreSQL
3. Create SQLModel models (User, Task)
4. Implement JWT verification middleware
5. Create health check endpoint
6. Create task CRUD endpoints
7. Test backend startup and health check

**Verification**: Run `uvicorn main:app --reload` and verify health check responds within 2 seconds

### Phase E: Integration Testing (Priority P5)

**Goal**: Verify end-to-end functionality

**Key Activities**:
1. Test JWT authentication flow from frontend to backend
2. Test task CRUD operations
3. Verify CORS configuration
4. Test error handling
5. Verify database connection and queries
6. Test responsive design on different viewports

**Verification**: Complete authentication and create/read/update/delete a task successfully

## Dependencies & Risks

### External Dependencies
- Neon PostgreSQL service availability (mitigated: graceful error handling)
- Better Auth library compatibility (mitigated: research phase verification)
- NPM/PyPI package availability (mitigated: lock files)

### Technical Risks
- **Risk**: Existing frontend/backend code may conflict with constitution requirements
  - **Mitigation**: Review and update existing code to align with constitution

- **Risk**: Environment variable mismatches between frontend and backend
  - **Mitigation**: Clear .env.example documentation and validation

- **Risk**: CORS issues between separate frontend/backend services
  - **Mitigation**: Research proper CORS configuration in Phase 0

### Timeline Risks
- **Risk**: Cleanup may accidentally remove necessary files
  - **Mitigation**: Review git status before cleanup, commit current state first

## Success Metrics

Based on spec success criteria:

- **Structure**: Root directory contains <10 files (excluding hidden dirs)
- **Frontend**: Starts in <5 seconds, UI is responsive
- **Backend**: Starts in <2 seconds, health check responds
- **Cleanup**: 0 .py test files in root directory
- **Setup**: New developer can set up project in <10 minutes
- **Documentation**: All environment variables documented in .env.example
- **Authentication**: JWT flow works end-to-end
- **Database**: Connection established successfully

## Next Steps

After this plan is approved:

1. **Generate Tasks**: Run `/sp.tasks` to convert implementation phases into actionable tasks
2. **Execute Tasks**: Follow TDD workflow (if applicable) or direct implementation
3. **Validate**: Verify all success metrics are met
4. **Document**: Update README.md with final setup instructions
5. **Commit**: Create PR with all changes

---

**Plan Status**: Ready for Phase 0 (Research)
**Constitutional Compliance**: ✅ Verified
**Blockers**: None
