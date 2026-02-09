// Protected Route Component
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI } from '../api/auth_api';
import { isTokenExpired, refreshToken } from '../lib/auth';

const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null); // null = checking, true/false = result
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // First check if token exists and is not expired
        if (!localStorage.getItem('better-auth-token')) {
          setIsAuthenticated(false);
          router.push('/login');
          return;
        }

        if (isTokenExpired()) {
          // Try to refresh the token
          const refreshed = await refreshToken();
          if (!refreshed) {
            // If refresh failed, clear tokens and redirect to login
            localStorage.removeItem('better-auth-token');
            localStorage.removeItem('better-auth-token-expiry');
            setIsAuthenticated(false);
            router.push('/login');
            return;
          }
        }

        // Token exists and is valid, verify with backend
        await authAPI.getProfile();
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Auth verification failed:', error);
        // Clear any invalid tokens
        localStorage.removeItem('better-auth-token');
        localStorage.removeItem('better-auth-token-expiry');
        setIsAuthenticated(false);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  if (loading || isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Checking authentication...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirect happens in useEffect
  }

  return children;
};

export default ProtectedRoute;