// Frontend authentication configuration using Better Auth
// This is a simplified representation - actual Better Auth implementation may vary

// Import Better Auth client
import { initClient } from "better-auth/client";
import { reactHooks } from "better-auth/react";

// Initialize Better Auth client
const client = initClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});

// Initialize React hooks
export const { signIn, signOut, useSession } = reactHooks(client);

// Function to get auth token from Better Auth
export const getAuthToken = () => {
  // In a real implementation, this would retrieve the token from Better Auth
  if (typeof window !== 'undefined') {
    return localStorage.getItem('better-auth-token');
  }
  return null;
};

// Function to set auth token
export const setAuthToken = (token) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('better-auth-token', token);
    // Also store the token expiry time to handle refresh
    const payload = JSON.parse(atob(token.split('.')[1]));
    localStorage.setItem('better-auth-token-expiry', payload.exp * 1000);
  }
};

// Function to remove auth token
export const removeAuthToken = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('better-auth-token');
    localStorage.removeItem('better-auth-token-expiry');
  }
};

// Function to check if token is expired
export const isTokenExpired = () => {
  if (typeof window !== 'undefined') {
    const expiryTime = localStorage.getItem('better-auth-token-expiry');
    if (expiryTime) {
      return Date.now() > parseInt(expiryTime);
    }
  }
  return true; // Assume expired if no expiry time found
};

// Function to refresh token (would call backend refresh endpoint)
export const refreshToken = async () => {
  // This would call the backend refresh endpoint in a real implementation
  // For now, we'll return false to indicate refresh is not possible
  return false;
};

// Export the client for use in API calls
export default client;