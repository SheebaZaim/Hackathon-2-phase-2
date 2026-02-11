/**
 * Type definitions for Todo App backend API
 * Matches backend models defined in backend/src/models.py
 */

export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface Task {
  id: string;
  title: string;
  completed: boolean;
  priority?: string | null;
  due_date?: string | null;
  category?: string | null;
  user_id: string;
  created_at: string;
  updated_at: string | null;
}

export interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  database: 'connected' | 'disconnected';
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  priority?: string;
  due_date?: string;
  category?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  completed?: boolean;
  description?: string;
  priority?: string;
  due_date?: string;
  category?: string;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  page?: number;
  limit?: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface ErrorResponse {
  detail: string;
}
