# Todo App - Project Overview

**Project Type**: Multi-user web application
**Phase**: II - Hackathon Project
**Status**: In Development
**Constitution Version**: 1.0.0

## Purpose

Convert a console-based Todo app into a secure, multi-user full-stack web application with authentication and data persistence.

## Constitution

This project is governed by strict architectural rules defined in [sp.constitution.md](./sp.constitution.md).

**Key Principles:**
- **Fixed Technology Stack**: No deviations allowed
- **Spec-Driven Development**: All code originates from specifications
- **Agentic Development**: Claude Code performs all coding tasks
- **Constitution Compliance**: All work must pass compliance checks

## Technology Stack (Fixed)

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend Framework | Next.js (App Router) | 16+ |
| Backend Framework | Python FastAPI | Latest |
| ORM | SQLModel | Latest |
| Database | Neon Serverless PostgreSQL | Latest |
| Authentication | Better Auth + JWT | Latest |

## Architecture Constraints

### Separation of Concerns
- Frontend and backend must be separate services
- No tight coupling between services
- Independent deployment capability

### Authentication
- Better Auth runs **only** on frontend
- Backend is **stateless** (no server-side sessions)
- JWT is the **only** authentication mechanism between services
- Shared secret configured via `BETTER_AUTH_SECRET`

### Communication
- RESTful APIs for all frontend-backend communication
- Proper error handling with meaningful status codes
- CORS configured to allow frontend origin only

### Security
- All sensitive data encrypted at rest and in transit
- JWT tokens stored securely (httpOnly cookies)
- Authorization header for all authenticated requests
- Stateless session management with token expiration

## Project Structure

```
todo-app/
├── frontend/           # Next.js 16+ application
├── backend/            # FastAPI application
├── specs/             # Feature specifications
│   ├── sp.constitution.md    # This constitution
│   ├── overview.md           # This file
│   └── ###-feature-name/     # Feature directories
│       ├── spec.md           # Feature specification
│       ├── plan.md           # Implementation plan
│       ├── tasks.md          # Task breakdown
│       ├── research.md       # Technical research
│       ├── data-model.md     # Database schema
│       └── contracts/        # API contracts
├── .specify/          # Spec-kit tooling
├── .spec-kit/         # Spec-kit configuration
└── README.md          # Project documentation
```

## Development Workflow

1. **Specification** (`/sp.specify`): Create feature specification
2. **Planning** (`/sp.plan`): Generate implementation plan
3. **Tasks** (`/sp.tasks`): Break down into actionable tasks
4. **Implementation** (`/sp.implement`): Execute tasks
5. **Validation**: Verify constitution compliance

## Features

### Current Features (Phase II)
- ✅ Project structure cleanup
- ✅ Essential configuration files
- 🔄 Frontend with Better Auth (in progress)
- 🔄 Backend with FastAPI + SQLModel (in progress)

### Planned Features
- User registration and login
- Task CRUD operations
- Task completion tracking
- Responsive UI (mobile/tablet/desktop)
- User data isolation
- RESTful API with documentation

## Governance

All development activities must comply with the constitution:
- Technology stack is fixed (no substitutions)
- All changes require formal specifications
- Code reviews verify constitutional compliance
- Amendments require stakeholder approval

## Resources

- **Constitution**: [specs/sp.constitution.md](./sp.constitution.md)
- **Setup Guide**: [README.md](../README.md)
- **API Documentation**: http://localhost:8000/docs (when running)
- **Specifications**: [specs/](.)

## Contributing

This project follows spec-driven development:
1. All features must have specifications
2. No manual coding (Claude Code only)
3. Constitution compliance is mandatory
4. Use feature branches: `###-feature-name`

---

**Last Updated**: 2026-02-09
**Maintained By**: Development Team
**Contact**: See project repository
