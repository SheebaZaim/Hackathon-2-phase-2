// hooks/useAuth.js
import { useState, useEffect, createContext, useContext } from 'react';
import { authService } from '../services/authService';

// Create Auth context
const AuthContext = createContext();

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isInitialized, setIsInitialized] = useState(false);

  // Check for existing token on mount
  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    // Check if we're on the client side (not during SSR)
    if (typeof window !== 'undefined') {
      try {
        const token = localStorage.getItem('auth_token');
        if (token) {
          // Verify token is not expired
          const isExpired = await authService.refreshToken();
          if (isExpired) {
            // Token is expired, remove it
            localStorage.removeItem('auth_token');
            localStorage.removeItem('auth_token_expiration');
          } else {
            // Token is valid, fetch user profile
            await fetchUserProfile();
          }
        }
      } catch (error) {
        console.error('Error in auth initialization:', error);
      } finally {
        setLoading(false);
        setIsInitialized(true);
      }
    } else {
      // If we're not on the client side (during SSR), set loading to false
      setLoading(false);
      setIsInitialized(true);
    }
  };

  const fetchUserProfile = async () => {
    try {
      const profile = await authService.getProfile();
      setUser(profile);
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // If profile fetch fails, clear the token
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_token_expiration');
      setUser(null);
    }
  };

  const login = async (email, password) => {
    try {
      // Only run on client side
      if (typeof window !== 'undefined') {
        const response = await authService.login({ email, password });
        if (response.access_token) {
          localStorage.setItem('auth_token', response.access_token);
          // Decode token to get user data
          await fetchUserProfile(); // Fetch full user profile from backend
          return { success: true, user: response };
        }
      }
    } catch (error) {
      return { success: false, message: error.message };
    }
  };

  const register = async (userData) => {
    try {
      // Only run on client side
      if (typeof window !== 'undefined') {
        const response = await authService.register(userData);
        if (response.access_token) {
          localStorage.setItem('auth_token', response.access_token);
          // Decode token to get user data
          await fetchUserProfile(); // Fetch full user profile from backend
          return { success: true, user: response };
        }
      }
    } catch (error) {
      return { success: false, message: error.message };
    }
  };

  const logout = async () => {
    try {
      // Only run on client side
      if (typeof window !== 'undefined') {
        await authService.logout();
        setUser(null);
      }
    } catch (error) {
      console.error('Error during logout:', error);
      // Even if backend logout fails, clear local state
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_token_expiration');
        setUser(null);
      }
    }
  };

  const value = {
    user,
    loading,
    isInitialized,
    login,
    register,
    logout,
    fetchUserProfile
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};