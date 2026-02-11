/**
 * useTasks Hook
 * Custom React hook for managing task CRUD operations
 */

import { useState, useEffect, useCallback } from 'react';
import { taskAPI } from '@/lib/api-client';
import type { Task, TaskUpdateRequest, TaskCreateRequest } from '@/lib/types';

type FilterType = 'all' | 'active' | 'completed';

interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  createTask: (data: TaskCreateRequest) => Promise<void>;
  updateTask: (id: string, data: TaskUpdateRequest) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  toggleTask: (id: string) => Promise<void>;
  reload: () => Promise<void>;
}

/**
 * Custom hook for task management with filtering and CRUD operations
 * @param filter - Filter type: 'all', 'active', or 'completed'
 * @returns Task data and CRUD methods
 */
export function useTasks(filter: FilterType = 'all'): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * Load tasks from backend based on current filter
   */
  const loadTasks = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Determine completed filter value
      const completed = filter === 'completed' ? true :
                       filter === 'active' ? false : undefined;

      const data = await taskAPI.list(completed);
      setTasks(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load tasks';
      setError(errorMessage);
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  /**
   * Create a new task
   * @param data - Task creation data
   */
  const createTask = async (data: TaskCreateRequest): Promise<void> => {
    try {
      const newTask = await taskAPI.create(data);

      // Only add to list if it matches current filter
      if (filter === 'all' || (filter === 'active' && !newTask.completed)) {
        setTasks(prevTasks => [...prevTasks, newTask]);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create task';
      setError(errorMessage);
      throw err;
    }
  };

  /**
   * Update an existing task
   * @param id - Task ID
   * @param data - Fields to update
   */
  const updateTask = async (id: string, data: TaskUpdateRequest): Promise<void> => {
    try {
      const updatedTask = await taskAPI.update(id, data);

      // Update task in list or remove if no longer matches filter
      setTasks(prevTasks => {
        const shouldKeep = filter === 'all' ||
                          (filter === 'active' && !updatedTask.completed) ||
                          (filter === 'completed' && updatedTask.completed);

        if (shouldKeep) {
          return prevTasks.map(t => t.id === id ? updatedTask : t);
        } else {
          // Remove from list if filter no longer matches
          return prevTasks.filter(t => t.id !== id);
        }
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update task';
      setError(errorMessage);
      throw err;
    }
  };

  /**
   * Delete a task
   * @param id - Task ID
   */
  const deleteTask = async (id: string): Promise<void> => {
    try {
      await taskAPI.delete(id);
      setTasks(prevTasks => prevTasks.filter(t => t.id !== id));
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete task';
      setError(errorMessage);
      throw err;
    }
  };

  /**
   * Toggle task completion status
   * @param id - Task ID
   */
  const toggleTask = async (id: string): Promise<void> => {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    await updateTask(id, { completed: !task.completed });
  };

  /**
   * Reload tasks (useful after external changes)
   */
  const reload = async (): Promise<void> => {
    await loadTasks();
  };

  // Load tasks when filter changes
  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  return {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleTask,
    reload,
  };
}
