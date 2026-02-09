    <!-- SYNC IMPACT REPORT
    Version change: 1.0.0 → 1.0.0 (initial creation)
    Added sections: Project Scope, Development Methodology, Fixed Technology Stack, Architecture Constraints, Authentication & Security Rules
    Removed sections: None (completely new content)
    Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
    Follow-up TODOs: None
    -->
    check this constitution file and make other sp.files like task,plan,specify files and make project professional according to constitution file  # Todo App Phase II Constitution
    ## Project Scope
    This is Phase II of a hackathon project with the goal to convert a console Todo app into a secure multi-user full-stack web app. The application must support multiple users with individual task lists, authentication, and data persistence.

    ## Development Methodology
    Spec-Driven Development is enforced throughout the project. All implementation must originate from specifications in the /specs directory. Agentic Dev Stack workflow is required with Claude Code performing all coding tasks. No manual coding by humans is permitted. All work must originate from specs and plans, ensuring traceability and consistency.

    ## Fixed Technology Stack
    The technology stack is fixed and must be adhered to without deviation:
    - Frontend: Next.js 16+ (App Router)
    - Backend: Python FastAPI
    - ORM: SQLModel
    - Database: Neon Serverless PostgreSQL
    - Authentication: Better Auth + JWT

    ## Architecture Constraints
    The frontend and backend must remain as separate services with no tight coupling. The backend must be stateless for authentication purposes. JWT is the only authentication mechanism allowed between services. All communication between frontend and backend must be RESTful APIs with proper error handling.

    ## Authentication & Security Rules
    Better Auth must run only on the frontend to handle user registration and login flows. Upon successful authentication, JWT tokens must be issued and stored securely. JWT tokens must be attached to the Authorization header for all authenticated requests to the backend. The backend must verify JWT tokens using a shared secret. The shared secret must be configured via BETTER_AUTH_SECRET environment variable. All sensitive data must be encrypted at rest and in transit. Session management must be stateless with proper token expiration and refresh mechanisms.

    ## Governance

    All development activities must comply with this constitution. Amendments require formal documentation, stakeholder approval, and a migration plan if applicable. Code reviews must verify constitutional compliance before merging. All team members must acknowledge and follow these governance rules.

    **Version**: 1.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-01-26
    