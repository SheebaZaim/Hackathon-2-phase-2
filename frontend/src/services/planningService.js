// services/planningService.js
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/plannings`,
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

// Planning API functions
export const planningService = {
  // Get all school plannings for the current user
  getAllPlannings: async () => {
    try {
      const response = await apiClient.get('/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch plannings');
    }
  },

  // Get a specific planning by ID
  getPlanningById: async (planningId) => {
    try {
      const response = await apiClient.get(`/${planningId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch planning');
    }
  },

  // Create a new school planning
  createPlanning: async (planningData) => {
    try {
      const response = await apiClient.post('/', planningData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to create planning');
    }
  },

  // Update an existing planning
  updatePlanning: async (planningId, planningData) => {
    try {
      const response = await apiClient.put(`/${planningId}`, planningData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to update planning');
    }
  },

  // Delete a planning
  deletePlanning: async (planningId) => {
    try {
      const response = await apiClient.delete(`/${planningId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to delete planning');
    }
  }
};