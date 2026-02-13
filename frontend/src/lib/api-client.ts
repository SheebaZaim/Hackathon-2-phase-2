/**
 * Backend API Client
 * Provides type-safe methods to interact with FastAPI backend at http://localhost:8000
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import type { Task, HealthStatus, TaskCreateRequest, TaskUpdateRequest } from './types';

// Create axios instance with base configuration
const api: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage (will be set by Better Auth)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle 401 Unauthorized - redirect to login
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
      }
    }

    // Extract error message properly
    let errorMessage = 'An error occurred';

    if (error.response?.data) {
      const data = error.response.data as any;

      // Handle FastAPI validation errors (422)
      if (Array.isArray(data.detail)) {
        const validationErrors = data.detail.map((err: any) => {
          const field = err.loc ? err.loc[err.loc.length - 1] : 'field';
          return `${field}: ${err.msg}`;
        }).join(', ');
        errorMessage = validationErrors || 'Validation error';
      } else if (typeof data.detail === 'string') {
        errorMessage = data.detail;
      } else if (data.message) {
        errorMessage = data.message;
      } else if (data.error) {
        errorMessage = data.error;
      }
    } else if (error.message) {
      errorMessage = error.message;
    }

    console.error('API Error:', errorMessage, error);
    return Promise.reject(new Error(errorMessage));
  }
);

/**
 * Health Check API
 */
export const healthAPI = {
  /**
   * Check backend health and database connection
   * GET /health
   */
  check: async (): Promise<HealthStatus> => {
    const response = await api.get<HealthStatus>('/health');
    return response.data;
  },
};

/**
 * Task CRUD API
 */
export const taskAPI = {
  /**
   * List all tasks for authenticated user
   * GET /api/tasks
   * @param completed - Optional filter: true for completed, false for active, undefined for all
   * @param page - Page number for pagination (default: 1)
   * @param limit - Items per page (default: 100)
   */
  list: async (completed?: boolean, page: number = 1, limit: number = 100): Promise<Task[]> => {
    const params: any = { page, limit };
    if (completed !== undefined) {
      params.completed = completed;
    }
    const response = await api.get<TaskListResponse>('/api/tasks', { params });
    return response.data.tasks; // Extract tasks array from response
  },

  /**
   * Create a new task
   * POST /api/tasks
   * @param data - Task creation data
   */
  create: async (data: TaskCreateRequest): Promise<Task> => {
    const response = await api.post<Task>('/api/tasks', data);
    return response.data;
  },

  /**
   * Get a single task by ID
   * GET /api/tasks/{task_id}
   * @param id - Task ID
   */
  get: async (id: string): Promise<Task> => {
    const response = await api.get<Task>(`/api/tasks/${id}`);
    return response.data;
  },

  /**
   * Update a task
   * PUT /api/tasks/{task_id}
   * @param id - Task ID
   * @param data - Fields to update (title and/or completed)
   */
  update: async (id: string, data: TaskUpdateRequest): Promise<Task> => {
    const response = await api.put<Task>(`/api/tasks/${id}`, data);
    return response.data;
  },

  /**
   * Delete a task
   * DELETE /api/tasks/{task_id}
   * @param id - Task ID
   */
  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/tasks/${id}`);
  },
};

export default api;
