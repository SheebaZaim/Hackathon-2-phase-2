---
name: auth-skill
description: Use this skill for managing user authentication and authorization securely. Implements signup, login, logout, RBAC, JWT/session management, password hashing, and OAuth integration.
---

# Auth Agent Skill

## Instructions
1. Implement secure user authentication workflows (signup, login, logout).  
2. Configure JWT and/or session-based authentication with proper expiration and refresh.  
3. Enforce role-based access control (RBAC) and permission validation for protected routes.  
4. Hash and verify passwords using bcrypt or argon2.  
5. Integrate OAuth or third-party login providers when needed.  
6. Handle environment variables securely for secrets, keys, and tokens.  
7. Ensure authentication logic is separate from business logic.  
8. Validate input and prevent security vulnerabilities (e.g., SQL injection).  

## Examples
- Implement signup endpoint with password hashing and JWT token issuance.  
- Validate user roles before granting access to admin-only routes.  
- Refresh JWT token automatically before expiration.  
- Integrate Google OAuth login in a FastAPI route.  
