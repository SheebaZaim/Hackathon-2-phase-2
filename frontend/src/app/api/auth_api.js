// Frontend API service for authentication with JWT handling

import axios from 'axios';

// Base API URL for backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API functions
export const authAPI = {
  // Login function
  login: async (email, password) => {
    const response = await api.post('/api/v1/auth/login', { email, password });
    const { access_token } = response.data;

    // Store the token in localStorage
    localStorage.setItem('auth_token', access_token);

    return response.data;
  },

  // Register function
  register: async (email, password) => {
    const response = await api.post('/api/v1/auth/register', { email, password });
    const { access_token } = response.data;

    // Store the token in localStorage
    localStorage.setItem('auth_token', access_token);

    return response.data;
  },

  // Logout function
  logout: async () => {
    try {
      await api.post('/api/v1/auth/logout');
    } finally {
      // Remove token regardless of API response
      localStorage.removeItem('auth_token');
    }
  },

  // Get user profile
  getProfile: async () => {
    const response = await api.get('/api/v1/auth/profile');
    return response.data;
  }
};