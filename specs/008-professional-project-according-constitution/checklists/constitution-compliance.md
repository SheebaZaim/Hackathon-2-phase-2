# Constitution Compliance Checklist: Professional Project According to Constitution

**Feature**: Professional Project According to Constitution
**Created**: 2026-02-09
**Status**: Active

## Overview
This checklist validates that all implementation follows the constitution requirements as defined in `specs/sp.constitution.md`.

## Technology Stack Compliance

- [ ] **Frontend**: Next.js 16+ (App Router) is used as specified in constitution
- [ ] **Backend**: Python FastAPI is used as specified in constitution
- [ ] **ORM**: SQLModel is used as specified in constitution
- [ ] **Database**: Neon Serverless PostgreSQL is used as specified in constitution
- [ ] **Authentication**: Better Auth + JWT is used as specified in constitution

## Architecture Constraints

- [ ] Frontend and backend remain as separate services with no tight coupling
- [ ] Backend is stateless for authentication purposes
- [ ] JWT is the only authentication mechanism allowed between services
- [ ] All communication between frontend and backend uses RESTful APIs with proper error handling

## Authentication & Security Rules

- [ ] Better Auth runs only on the frontend to handle user registration and login flows
- [ ] Upon successful authentication, JWT tokens are issued and stored securely
- [ ] JWT tokens are attached to the Authorization header for all authenticated requests to the backend
- [ ] Backend verifies JWT tokens using a shared secret via BETTER_AUTH_SECRET environment variable
- [ ] All sensitive data is encrypted at rest and in transit
- [ ] Session management is stateless with proper token expiration and refresh mechanisms

## Development Methodology

- [ ] Spec-Driven Development is enforced throughout the project
- [ ] All implementation originates from specifications in the /specs directory
- [ ] Agentic Dev Stack workflow is used with Claude Code performing coding tasks
- [ ] All work originates from specs and plans, ensuring traceability and consistency

## Governance

- [ ] All development activities comply with the constitution
- [ ] Code reviews verify constitutional compliance before merging
- [ ] Team members follow governance rules

## Template Updates

- [ ] .specify/templates/spec-template.md updated to reflect constitution requirements
- [ ] .specify/templates/plan-template.md updated to include constitution checks
- [ ] .specify/templates/tasks-template.md updated to enforce constitution compliance

## Implementation Verification

- [ ] All functional requirements (FR-001 through FR-010) are implemented
- [ ] Key entities (User, Todo List, Task, Authentication Token) are properly defined
- [ ] Success criteria (SC-001 through SC-006) are met
- [ ] User stories 1, 2, and 3 are fully implemented and tested
- [ ] Edge cases are properly handled

## Quickstart Validation

- [ ] Both frontend and backend servers can be started successfully
- [ ] Authentication flow works with Better Auth and JWT tokens
- [ ] Database connects properly to Neon Serverless PostgreSQL
- [ ] API endpoints are accessible and functioning
- [ ] User data isolation is maintained between different users