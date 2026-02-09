// services/authService.js
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      // Check if token is expired before sending request
      if (isTokenExpired(token)) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_token_expiration');
        window.location.href = '/login';
        return Promise.reject(new Error('Token expired'));
      }
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, clear it and redirect to login
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_token_expiration');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Helper function to check if JWT token is expired
function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp < currentTime;
  } catch (error) {
    console.error('Error decoding token:', error);
    return true; // Assume expired if we can't decode
  }
}

// Authentication API functions
export const authService = {
  // Register a new user
  register: async (userData) => {
    try {
      const response = await apiClient.post('/api/v1/auth/register', {
        email: userData.email,
        password: userData.password,
        first_name: userData.first_name,
        last_name: userData.last_name
      });
      // Store token if registration is successful and auto-login is desired
      if (response.data.access_token) {
        localStorage.setItem('auth_token', response.data.access_token);
        // Also store token expiration time for proactive refresh
        const payload = JSON.parse(atob(response.data.access_token.split('.')[1]));
        localStorage.setItem('auth_token_expiration', payload.exp.toString());
      }
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Registration failed';
      throw new Error(errorMessage);
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      const response = await apiClient.post('/api/v1/auth/login', {
        email: credentials.email,
        password: credentials.password
      });
      // Store token
      if (response.data.access_token) {
        localStorage.setItem('auth_token', response.data.access_token);
        // Also store token expiration time for proactive refresh
        const payload = JSON.parse(atob(response.data.access_token.split('.')[1]));
        localStorage.setItem('auth_token_expiration', payload.exp.toString());
      }
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Login failed';
      throw new Error(errorMessage);
    }
  },

  // Logout user
  logout: async () => {
    try {
      // Clear token from localStorage
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_token_expiration');
      
      // Optionally notify backend about logout (for refresh token invalidation)
      // await apiClient.post('/api/v1/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
      // Even if backend logout fails, clear local token
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_token_expiration');
    }
  },

  // Get current user profile
  getProfile: async () => {
    try {
      const response = await apiClient.get('/api/v1/auth/profile');
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to fetch profile';
      throw new Error(errorMessage);
    }
  },
  
  // Refresh token if needed
  refreshToken: async () => {
    // In a real implementation, you would use a refresh token here
    // For now, we'll just return a boolean indicating if the token needs refresh
    const token = localStorage.getItem('auth_token');
    if (!token) return false;
    
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    const timeUntilExpiration = payload.exp - currentTime;
    
    // If token expires in less than 5 minutes, consider it needs refresh
    return timeUntilExpiration < 300;
  }
};