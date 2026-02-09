# Tasks: Project Cleanup and Functional Setup

**Input**: Design documents from `/specs/001-cleanup-functional-project/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Not requested in specification - manual testing only per plan.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Web application structure (per plan.md):
- **Frontend**: `frontend/src/`
- **Backend**: `backend/src/`
- **Root**: Project root for cleanup tasks

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify current project state and prepare for cleanup

- [X] T001 Review current git status and create backup branch before cleanup
- [X] T002 Document current file structure (count files in root, list directories)

---

## Phase 2: User Story 1 - Project Structure Cleanup (Priority: P1) 🎯 MVP

**Goal**: Remove all unnecessary files and directories, keeping only essential components for a functional multi-user todo application per constitution

**Independent Test**: Verify project directory contains only frontend/, backend/, specs/, .specify/, .spec-kit/, and essential root config files. Count files in root (should be <10 excluding hidden dirs). No .py test scripts in root.

### Implementation for User Story 1

- [X] T003 [P] [US1] Delete test script: check_neon_connection.py from root
- [X] T004 [P] [US1] Delete test script: create_tables_directly.py from root
- [X] T005 [P] [US1] Delete test script: simple_db_test.py from root
- [X] T006 [P] [US1] Delete test script: test_api.py from root
- [X] T007 [P] [US1] Delete test script: test_db_creation.py from root
- [X] T008 [P] [US1] Delete test script: test_server.py from root
- [X] T009 [P] [US1] Delete test script: validate_setup.py from root
- [X] T010 [P] [US1] Delete test script: verify_todo_app.py from root
- [X] T011 [P] [US1] Delete summary file: BACKEND_IMPLEMENTATION_SUMMARY.md from root
- [X] T012 [P] [US1] Delete summary file: FRONTEND_IMPLEMENTATION_SUMMARY.md from root
- [X] T013 [P] [US1] Delete summary file: IMPLEMENTATION_SUMMARY.md from root
- [X] T014 [P] [US1] Delete temporary file: QWEN.md from root
- [X] T015 [P] [US1] Remove directory: backend_env/ from root
- [X] T016 [P] [US1] Remove directory: backend_env_py311/ from root
- [X] T017 [P] [US1] Remove directory: -p/ from root (if exists)
- [X] T018 [P] [US1] Remove directory: config/ from root
- [X] T019 [P] [US1] Remove directory: docs/ from root
- [X] T020 [P] [US1] Remove directory: tests/ from root
- [X] T021 [P] [US1] Remove directory: tasks/ from root
- [X] T022 [P] [US1] Remove directory: public/ from root (if in root, not frontend/public)
- [X] T023 [P] [US1] Remove directory: node_modules/ from root (if in root, not frontend/node_modules)
- [X] T024 [P] [US1] Remove files: mock-api-server.js, package.json, package-lock.json from root (workspace scripts not needed)
- [X] T025 [US1] Verify root directory contains fewer than 10 files (excluding hidden directories)
- [X] T026 [US1] Verify only CLAUDE.md, README.md, .gitignore remain in root (plus hidden dirs/files)

**Checkpoint**: Root directory is clean - only essential files remain

---

## Phase 3: User Story 2 - Essential Files Verification (Priority: P2)

**Goal**: Ensure all required configuration files and documentation exist and are properly configured per constitution

**Independent Test**: Check presence of .env.example in frontend and backend with documented variables. Verify package.json, requirements.txt exist. Verify README.md has setup instructions.

### Implementation for User Story 2

- [ ] T027 [P] [US2] Create frontend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL
- [ ] T028 [P] [US2] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL
- [ ] T029 [US2] Verify frontend/package.json exists with required dependencies (Next.js 16+, Better Auth, React, TailwindCSS)
- [ ] T030 [US2] Verify backend/requirements.txt exists with required dependencies (FastAPI, SQLModel, psycopg2, python-jose, passlib)
- [ ] T031 [US2] Update README.md with project overview, architecture, and setup instructions based on quickstart.md
- [ ] T032 [US2] Verify CLAUDE.md exists and contains project instructions
- [ ] T033 [US2] Create specs/overview.md with project overview and constitution reference
- [ ] T034 [US2] Verify .gitignore includes .env, node_modules, __pycache__, venv, backend_env

**Checkpoint**: All essential configuration files exist and are documented

---

## Phase 4: User Story 3 - Frontend Functionality (Priority: P3)

**Goal**: Ensure frontend is functional with Better Auth, simple and attractive UI, responsive design

**Independent Test**: Run `npm run dev` in frontend/ and verify application loads within 5 seconds with authentication screens. UI should be responsive on mobile, tablet, desktop.

### Implementation for User Story 3

- [ ] T035 [US3] Verify Next.js 16+ configuration in frontend/next.config.js (App Router enabled)
- [ ] T036 [US3] Verify TypeScript configuration in frontend/tsconfig.json
- [ ] T037 [P] [US3] Implement Better Auth configuration in frontend/src/lib/auth.ts per research.md patterns
- [ ] T038 [P] [US3] Create API client in frontend/src/lib/api-client.ts with fetch, error handling, auth headers
- [ ] T039 [P] [US3] Create TypeScript types in frontend/src/lib/types.ts (User, Task, API responses)
- [ ] T040 [P] [US3] Setup TailwindCSS in frontend/src/styles/globals.css with responsive utilities
- [ ] T041 [US3] Create homepage in frontend/src/app/page.tsx (redirect to auth or dashboard based on session)
- [ ] T042 [P] [US3] Create signin page in frontend/src/app/auth/signin/page.tsx (email + password form)
- [ ] T043 [P] [US3] Create signup page in frontend/src/app/auth/signup/page.tsx (email + password form)
- [ ] T044 [P] [US3] Create authentication UI components in frontend/src/components/auth/ (AuthForm, AuthButton)
- [ ] T045 [US3] Create dashboard page in frontend/src/app/dashboard/page.tsx (protected route with task list)
- [ ] T046 [P] [US3] Create task UI components in frontend/src/components/tasks/ (TaskCard, TaskList, TaskForm)
- [ ] T047 [P] [US3] Create UI primitives in frontend/src/components/ui/ (Button, Input, Card) with responsive Tailwind classes
- [ ] T048 [US3] Implement responsive design breakpoints (mobile-first: sm, md, lg, xl) per research.md
- [ ] T049 [US3] Test frontend startup time (<5 seconds) and UI responsiveness on different viewports
- [ ] T050 [US3] Verify Better Auth signup/signin flows work correctly

**Checkpoint**: Frontend is functional with authentication and responsive UI

---

## Phase 5: User Story 4 - Backend Functionality (Priority: P4)

**Goal**: Ensure backend is functional with FastAPI, SQLModel, Neon PostgreSQL, JWT verification

**Independent Test**: Run `uvicorn src.main:app --reload` in backend/ and verify health endpoint responds within 2 seconds. Database connection established. API docs available at /docs.

### Implementation for User Story 4

- [ ] T051 [P] [US4] Create database connection in backend/src/database/connection.py with Neon PostgreSQL (SSL required)
- [ ] T052 [P] [US4] Create database initialization script in backend/src/database/init_db.py (create tables)
- [ ] T053 [P] [US4] Create User model in backend/src/models/user.py with SQLModel (id, email, password_hash, timestamps)
- [ ] T054 [P] [US4] Create Task model in backend/src/models/task.py with SQLModel (id, user_id, title, description, completed, timestamps)
- [ ] T055 [P] [US4] Implement JWT verification middleware in backend/src/middleware/auth.py using python-jose per research.md
- [ ] T056 [P] [US4] Implement authentication service in backend/src/services/auth.py (JWT verification logic)
- [ ] T057 [P] [US4] Implement task service in backend/src/services/tasks.py (CRUD operations with user isolation)
- [ ] T058 [US4] Create health check endpoint in backend/src/api/health.py (GET /health with database status)
- [ ] T059 [P] [US4] Create task endpoints in backend/src/api/tasks.py (GET/POST/PUT/DELETE /api/tasks with auth middleware)
- [ ] T060 [US4] Create FastAPI application in backend/src/main.py with CORS middleware (allow frontend origin)
- [ ] T061 [US4] Configure CORS to allow frontend URL from environment variable FRONTEND_URL
- [ ] T062 [US4] Test backend startup time (<2 seconds) and health check response
- [ ] T063 [US4] Test database connection with Neon PostgreSQL (verify SSL connection)
- [ ] T064 [US4] Test JWT verification with sample token
- [ ] T065 [US4] Verify API documentation accessible at /docs (auto-generated by FastAPI)

**Checkpoint**: Backend is functional with database, authentication, and API endpoints

---

## Phase 6: Integration & End-to-End Validation

**Goal**: Verify frontend and backend work together correctly with full authentication flow

**Independent Test**: Complete signup → signin → create task → update task → delete task → logout flow. Verify second user has isolated tasks.

- [ ] T066 Test complete authentication flow: signup → JWT token generated → stored in cookie
- [ ] T067 Test authentication flow: signin → JWT token → redirect to dashboard
- [ ] T068 Test API call flow: frontend sends request with Authorization header → backend verifies JWT → returns data
- [ ] T069 Test task CRUD: create task via frontend → stored in database → retrieved via API
- [ ] T070 Test task CRUD: update task completion status → persisted in database
- [ ] T071 Test task CRUD: delete task → removed from database
- [ ] T072 Test user isolation: create second user → verify cannot see first user's tasks
- [ ] T073 Test error handling: invalid JWT token → 401 Unauthorized response
- [ ] T074 Test error handling: missing environment variables → clear error messages
- [ ] T075 Test error handling: database connection failure → graceful error with message
- [ ] T076 Test CORS: verify frontend can make requests to backend without CORS errors
- [ ] T077 Test responsive UI: verify interface works on mobile (375px), tablet (768px), desktop (1920px)

**Checkpoint**: All user stories are integrated and working end-to-end

---

## Phase 7: Constitution Compliance & Polish

**Purpose**: Verify all constitution requirements are met and finalize documentation

- [ ] T078 [P] Verify Next.js 16+ with App Router is used in frontend
- [ ] T079 [P] Verify Python FastAPI is used in backend
- [ ] T080 [P] Verify SQLModel ORM is used for database models
- [ ] T081 [P] Verify Neon Serverless PostgreSQL is connected (check DATABASE_URL format)
- [ ] T082 [P] Verify Better Auth + JWT are used for authentication
- [ ] T083 Confirm frontend and backend are separate services (different directories, separate configs)
- [ ] T084 Verify backend is stateless (no server-side session storage, JWT verification only)
- [ ] T085 Verify JWT is the only authentication mechanism between services
- [ ] T086 Verify RESTful API design with proper error handling (status codes, error messages)
- [ ] T087 Verify Better Auth runs only on frontend (no backend auth endpoints)
- [ ] T088 Verify JWT tokens are stored in httpOnly cookies (Better Auth default)
- [ ] T089 Verify Authorization header is used for authenticated API requests
- [ ] T090 Verify BETTER_AUTH_SECRET is shared between frontend and backend
- [ ] T091 Verify SSL/TLS encryption for database connection (sslmode=require in DATABASE_URL)
- [ ] T092 Verify stateless session management (no session table in database)
- [ ] T093 Update README.md with final architecture diagram and deployment notes
- [ ] T094 [P] Verify all environment variables are documented in .env.example files
- [ ] T095 [P] Verify quickstart.md setup time is <10 minutes (test with fresh clone)
- [ ] T096 Code cleanup: remove console.log, commented code, unused imports
- [ ] T097 [P] Add comments to complex code sections (auth middleware, JWT verification)
- [ ] T098 Final verification: run through all acceptance scenarios from spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup - must complete before other stories
- **User Story 2 (Phase 3)**: Depends on US1 (cleanup complete before verifying essential files)
- **User Story 3 (Phase 4)**: Depends on US1 and US2 (clean structure + essential files exist)
- **User Story 4 (Phase 5)**: Depends on US1 and US2 (clean structure + essential files exist)
  - US3 and US4 can proceed in parallel once US1 and US2 are complete
- **Integration (Phase 6)**: Depends on US3 and US4 both complete
- **Polish (Phase 7)**: Depends on Integration complete

### User Story Dependencies

- **User Story 1 (P1)**: BLOCKING - must complete first (cleanup before building)
- **User Story 2 (P2)**: Depends on US1 - creates essential files after cleanup
- **User Story 3 (P3)**: Depends on US1, US2 - can run parallel with US4
- **User Story 4 (P4)**: Depends on US1, US2 - can run parallel with US3

### Within Each User Story

- Cleanup tasks (T003-T024) can all run in parallel [P]
- Frontend file creation (T027, T037-T047) can run in parallel [P] within their groups
- Backend file creation (T051-T057, T059) can run in parallel [P] within their groups
- Verification tasks must run after implementation tasks complete

### Parallel Opportunities

**User Story 1 (Cleanup)**: All delete operations (T003-T024) can run in parallel

**User Story 2 (Essential Files)**: T027-T028 can run in parallel, T029-T034 can run in parallel

**User Story 3 (Frontend)**:
- T037-T040 can run in parallel (lib files)
- T042-T043 can run in parallel (auth pages)
- T044, T046-T047 can run in parallel (component groups)

**User Story 4 (Backend)**:
- T051-T054 can run in parallel (database + models)
- T055-T057 can run in parallel (middleware + services)
- T059 after T055 (endpoints need auth middleware)

**US3 and US4 together**: Once US1 and US2 complete, US3 (frontend) and US4 (backend) can be developed in parallel by different developers

---

## Parallel Example: User Story 1 (Cleanup)

```bash
# Launch all cleanup tasks together:
Task: "Delete test script: check_neon_connection.py from root"
Task: "Delete test script: create_tables_directly.py from root"
Task: "Delete test script: simple_db_test.py from root"
Task: "Delete test script: test_api.py from root"
Task: "Delete test script: test_db_creation.py from root"
Task: "Delete test script: test_server.py from root"
Task: "Delete test script: validate_setup.py from root"
Task: "Delete test script: verify_todo_app.py from root"
Task: "Delete summary file: BACKEND_IMPLEMENTATION_SUMMARY.md from root"
Task: "Delete summary file: FRONTEND_IMPLEMENTATION_SUMMARY.md from root"
Task: "Delete summary file: IMPLEMENTATION_SUMMARY.md from root"
Task: "Delete temporary file: QWEN.md from root"
Task: "Remove directory: backend_env/ from root"
Task: "Remove directory: backend_env_py311/ from root"
Task: "Remove directory: -p/ from root"
Task: "Remove directory: config/ from root"
Task: "Remove directory: docs/ from root"
Task: "Remove directory: tests/ from root"
Task: "Remove directory: tasks/ from root"
Task: "Remove directory: public/ from root"
Task: "Remove directory: node_modules/ from root"
Task: "Remove files: mock-api-server.js, package.json, package-lock.json from root"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 + 3 + 4)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: User Story 1 - Cleanup (T003-T026)
3. Complete Phase 3: User Story 2 - Essential Files (T027-T034)
4. Complete Phase 4: User Story 3 - Frontend (T035-T050)
5. Complete Phase 5: User Story 4 - Backend (T051-T065)
6. Complete Phase 6: Integration (T066-T077)
7. Complete Phase 7: Polish (T078-T098)
8. **STOP and VALIDATE**: Test complete application flow
9. Deploy/demo functional app

### Incremental Delivery

1. Complete Setup + US1 → Clean project structure
2. Add US2 → Essential files present → Can set up project
3. Add US3 → Frontend working → Can signup/signin
4. Add US4 → Backend working → Can create/manage tasks
5. Integration → Full app functional → Ready for use
6. Polish → Constitution compliant → Production ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + US1 (Cleanup) together
2. Team completes US2 (Essential Files) together
3. Once US2 is done:
   - Frontend Developer: User Story 3 (T035-T050)
   - Backend Developer: User Story 4 (T051-T065)
4. Both developers: Integration testing (T066-T077)
5. Team: Constitution compliance and polish (T078-T098)

---

## Task Summary

**Total Tasks**: 98 tasks
**Breakdown by Phase**:
- Setup: 2 tasks
- User Story 1 (P1 - Cleanup): 24 tasks (22 parallel)
- User Story 2 (P2 - Essential Files): 8 tasks (7 parallel groups)
- User Story 3 (P3 - Frontend): 16 tasks (11 parallel)
- User Story 4 (P4 - Backend): 15 tasks (9 parallel)
- Integration: 12 tasks
- Polish: 21 tasks (14 parallel)

**Parallel Opportunities**: 66 tasks marked [P] can run in parallel within their phase/group

**MVP Scope**: All 4 user stories are essential for a functional application:
- US1: Clean structure (foundation)
- US2: Essential configs (enables setup)
- US3: Frontend (user interface)
- US4: Backend (data persistence)

**Independent Test Criteria**:
- US1: Root has <10 files, no .py scripts
- US2: .env.example files exist with docs
- US3: Frontend starts in <5s, responsive UI
- US4: Backend starts in <2s, /health responds

---

## Notes

- All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [P] tasks = different files, can run in parallel
- [Story] labels: [US1], [US2], [US3], [US4] for traceability
- No automated tests (per plan.md - manual testing only)
- Each user story is independently testable per acceptance scenarios
- Constitution compliance verified in final phase
- Commit after each task group completion
- Verify at each checkpoint before proceeding
