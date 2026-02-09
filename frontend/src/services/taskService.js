// services/taskService.js
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/tasks`,
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
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Task API functions
export const taskService = {
  // Get all tasks for the current user
  getAllTasks: async () => {
    try {
      const response = await apiClient.get('/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch tasks');
    }
  },

  // Get a specific task by ID
  getTaskById: async (taskId) => {
    try {
      const response = await apiClient.get(`/${taskId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch task');
    }
  },

  // Create a new task
  createTask: async (taskData) => {
    try {
      const response = await apiClient.post('/', taskData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to create task');
    }
  },

  // Update an existing task
  updateTask: async (taskId, taskData) => {
    try {
      const response = await apiClient.put(`/${taskId}`, taskData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to update task');
    }
  },

  // Toggle task completion status
  toggleTaskCompletion: async (taskId) => {
    try {
      const response = await apiClient.patch(`/${taskId}/toggle`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to toggle task completion');
    }
  },

  // Delete a task
  deleteTask: async (taskId) => {
    try {
      const response = await apiClient.delete(`/${taskId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to delete task');
    }
  }
};