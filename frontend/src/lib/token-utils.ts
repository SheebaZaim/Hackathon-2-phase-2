/**
 * JWT Token Utilities
 * Extract and manage JWT tokens for backend API authentication
 */

/**
 * Store authentication token in localStorage
 * @param token - JWT token from Better Auth
 */
export function setAuthToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
  }
}

/**
 * Get authentication token from localStorage
 * @returns JWT token or null if not found
 */
export function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
}

/**
 * Remove authentication token from localStorage
 */
export function removeAuthToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
  }
}

/**
 * Check if user is authenticated
 * @returns true if auth token exists
 */
export function isAuthenticated(): boolean {
  return getAuthToken() !== null;
}

/**
 * Extract JWT token from Better Auth session
 * Better Auth provides the session with user data and token
 * @param session - Better Auth session object
 * @returns JWT token string or null
 */
export function extractTokenFromSession(session: any): string | null {
  // Better Auth session structure may vary
  // Check common locations for token
  if (!session) return null;

  // Try different possible locations
  if (session.token) return session.token;
  if (session.access_token) return session.access_token;
  if (session.jwt) return session.jwt;

  return null;
}
