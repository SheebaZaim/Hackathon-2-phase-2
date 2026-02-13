/**
 * Dashboard Page
 * Protected page for managing tasks
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getCurrentUser, logout, isAuthenticated } from '@/lib/auth-simple';
import { useTasks } from '@/hooks/useTasks';
import TaskListComponent from '@/components/tasks/TaskListComponent';
import TaskFormComponent from '@/components/tasks/TaskFormComponent';
import TaskFilter from '@/components/tasks/TaskFilter';

type FilterType = 'all' | 'active' | 'completed';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<{ email: string } | null>(null);
  const [filter, setFilter] = useState<FilterType>('all');
  const { tasks, loading, error, createTask, updateTask, deleteTask, toggleTask } = useTasks(filter);

  useEffect(() => {
    // Small delay to ensure token is loaded from localStorage
    const checkAuth = async () => {
      await new Promise(resolve => setTimeout(resolve, 50));

      // Check authentication
      if (!isAuthenticated()) {
        router.push('/login');
        return;
      }

      // Get user info
      const currentUser = getCurrentUser();
      if (currentUser) {
        setUser(currentUser);
      }
    };

    checkAuth();
  }, [router]);

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const handleEditTask = async (id: string, title: string) => {
    try {
      await updateTask(id, { title });
      // Task list will update automatically via the hook
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  if (!user) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">📝 Todo App</h1>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">{user.email}</span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - Centered */}
      <main className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Task Creation Form - Centered */}
          <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 text-center">Add New Task</h2>
            <TaskFormComponent onSubmit={createTask} />
          </div>

          {/* Task Filters - Centered */}
          <div className="mb-6 flex justify-center">
            <TaskFilter activeFilter={filter} onFilterChange={setFilter} />
          </div>

          {/* Task List - Table Format */}
          <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 text-center">
                {filter === 'all' && 'All Tasks'}
                {filter === 'active' && 'Active Tasks'}
                {filter === 'completed' && 'Completed Tasks'}
                <span className="ml-2 text-sm font-normal text-gray-500">
                  ({tasks.length} {tasks.length === 1 ? 'task' : 'tasks'})
                </span>
              </h2>
            </div>
            <TaskListComponent
              tasks={tasks}
              loading={loading}
              error={error}
              onToggle={toggleTask}
              onDelete={deleteTask}
              onEdit={handleEditTask}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
