# Teachers Planning App - Authentication & Security Specification

## Architecture
- Better Auth runs only on the frontend
- JWT issued post-login for backend authentication
- JWT stored securely in browser storage
- Backend verifies JWT using BETTER_AUTH_SECRET

## Authentication Flow

### Login Process
1. User enters credentials on frontend
2. Credentials sent to Better Auth for verification
3. Upon successful authentication, JWT is issued
4. JWT is stored securely in browser (preferably httpOnly cookie or secure localStorage)
5. JWT is attached to all subsequent backend requests as `Authorization: Bearer <token>`

### Backend Verification
1. Each protected endpoint validates the JWT using BETTER_AUTH_SECRET
2. Token expiration is checked
3. User identity is verified from token claims
4. Access is granted based on user role (teacher only)

## JWT Configuration
- Algorithm: HS256
- Expiration: 24 hours (configurable)
- Refresh strategy: Implement refresh token mechanism
- Claims: user ID, role, expiration, issuer

## Security Measures
- HTTPS required for all authentication
- Secure storage of JWT in browser
- Proper CORS configuration
- Rate limiting on authentication endpoints
- Input validation and sanitization
- Protection against CSRF and XSS attacks

## Token Storage
- Frontend: Secure storage mechanism (httpOnly cookies preferred)
- Avoid storing sensitive tokens in plain localStorage if possible
- Implement automatic token refresh before expiration

## Error Handling
- Proper error responses for invalid tokens
- Clear messaging for expired tokens
- Secure logout that clears all stored tokens
- Prevention of token replay attacks

## Session Management
- Stateless authentication using JWT
- Token refresh mechanism to extend session
- Secure logout functionality
- Automatic redirection to login on authentication failure

## Secret Management
- BETTER_AUTH_SECRET stored in environment variables
- Different secrets for development and production
- Regular rotation of secrets in production
- Access controls on secret storage