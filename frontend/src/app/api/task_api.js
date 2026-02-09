// Frontend API service for task management

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
    const token = localStorage.getItem('auth_token'); // Using consistent token name
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

// Task API functions
export const taskAPI = {
  // Get all tasks for the current user
  getTasks: async () => {
    const response = await api.get('/api/v1/tasks'); // Updated to match backend API route
    return response.data;
  },

  // Create a new task
  createTask: async (taskData) => {
    const response = await api.post('/api/v1/tasks', taskData); // Updated to match backend API route
    return response.data;
  },

  // Update a task
  updateTask: async (taskId, taskData) => {
    const response = await api.put(`/api/v1/tasks/${taskId}`, taskData); // Updated to match backend API route
    return response.data;
  },

  // Toggle task completion status
  toggleTask: async (taskId) => {
    // Use the PATCH endpoint that matches the backend implementation
    const response = await api.patch(`/api/v1/tasks/${taskId}/toggle`); // Updated to match backend API route
    return response.data;
  },

  // Delete a task
  deleteTask: async (taskId) => {
    const response = await api.delete(`/api/v1/tasks/${taskId}`); // Updated to match backend API route
    return response.data;
  },

  // Get a specific task
  getTaskById: async (taskId) => {
    const response = await api.get(`/api/v1/tasks/${taskId}`); // Updated to match backend API route
    return response.data;
  }
};