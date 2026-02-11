/**
 * TaskList Component - Table Format
 * Displays tasks in a clean, organized table
 */

'use client';

import React, { useState } from 'react';
import type { Task } from '@/lib/types';

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  onToggle: (id: string) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onEdit: (id: string, title: string) => Promise<void>;
}

export default function TaskListComponent({
  tasks,
  loading,
  error,
  onToggle,
  onDelete,
  onEdit,
}: TaskListProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getPriorityBadge = (priority: string | null | undefined) => {
    const p = priority || 'medium';
    const colors = {
      high: 'bg-red-100 text-red-700',
      medium: 'bg-yellow-100 text-yellow-700',
      low: 'bg-green-100 text-green-700',
    };
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${colors[p as keyof typeof colors] || colors.medium}`}>
        {p.charAt(0).toUpperCase() + p.slice(1)}
      </span>
    );
  };

  const handleToggle = async (id: string) => {
    setActionLoading(id);
    try {
      await onToggle(id);
    } finally {
      setActionLoading(null);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this task?')) {
      setActionLoading(id);
      try {
        await onDelete(id);
      } finally {
        setActionLoading(null);
      }
    }
  };

  const handleEditStart = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
  };

  const handleEditSave = async (id: string) => {
    const trimmedTitle = editTitle.trim();
    if (!trimmedTitle) {
      alert('Task title cannot be empty');
      return;
    }

    setActionLoading(id);
    try {
      await onEdit(id, trimmedTitle);
      setEditingId(null);
    } catch (err) {
      alert('Failed to update task');
    } finally {
      setActionLoading(null);
    }
  };

  const handleEditCancel = () => {
    setEditingId(null);
    setEditTitle('');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (error) {
    const errorMessage = typeof error === 'string' ? error : error?.message || 'Failed to load tasks';
    return (
      <div className="p-6 text-center">
        <div className="text-red-600 bg-red-50 rounded-lg p-4 border border-red-200">
          <p className="font-medium">Error loading tasks</p>
          <p className="text-sm mt-1">{errorMessage}</p>
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="p-12 text-center">
        <p className="text-gray-500 text-lg font-medium">No tasks found</p>
        <p className="text-gray-400 text-sm mt-2">Create your first task to get started!</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="bg-gray-50 border-b border-gray-200">
            <th className="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider w-12">
              Done
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Title
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Description
            </th>
            <th className="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider w-24">
              Priority
            </th>
            <th className="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider w-32">
              Due Date
            </th>
            <th className="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider w-32">
              Category
            </th>
            <th className="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider w-40">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {tasks.map((task) => (
            <tr key={task.id} className="hover:bg-gray-50 transition-colors">
              {/* Checkbox */}
              <td className="px-4 py-4 text-center">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => handleToggle(task.id)}
                  disabled={actionLoading === task.id}
                  className="w-5 h-5 text-green-600 rounded focus:ring-2 focus:ring-green-500 cursor-pointer disabled:cursor-not-allowed"
                />
              </td>

              {/* Title */}
              <td className="px-4 py-4">
                {editingId === task.id ? (
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') handleEditSave(task.id);
                      if (e.key === 'Escape') handleEditCancel();
                    }}
                    disabled={actionLoading === task.id}
                    className="w-full px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                    autoFocus
                  />
                ) : (
                  <div className={task.completed ? 'line-through text-gray-500' : 'text-gray-900'}>
                    <p className="font-medium">{task.title}</p>
                  </div>
                )}
              </td>

              {/* Description */}
              <td className="px-4 py-4">
                <p className={`text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'} max-w-xs truncate`}>
                  {task.description || '-'}
                </p>
              </td>

              {/* Priority */}
              <td className="px-4 py-4 text-center">
                {getPriorityBadge(task.priority)}
              </td>

              {/* Due Date */}
              <td className="px-4 py-4 text-center text-sm text-gray-600">
                {formatDate(task.due_date)}
              </td>

              {/* Category */}
              <td className="px-4 py-4 text-center">
                {task.category ? (
                  <span className="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-700">
                    {task.category}
                  </span>
                ) : (
                  <span className="text-gray-400">-</span>
                )}
              </td>

              {/* Actions */}
              <td className="px-4 py-4 text-center">
                {editingId === task.id ? (
                  <div className="flex gap-2 justify-center">
                    <button
                      onClick={() => handleEditSave(task.id)}
                      disabled={actionLoading === task.id}
                      className="px-3 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-300 transition-colors"
                    >
                      Save
                    </button>
                    <button
                      onClick={handleEditCancel}
                      disabled={actionLoading === task.id}
                      className="px-3 py-1 text-xs bg-gray-300 text-gray-700 rounded hover:bg-gray-400 disabled:bg-gray-200 transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                ) : (
                  <div className="flex gap-2 justify-center">
                    <button
                      onClick={() => handleEditStart(task)}
                      disabled={actionLoading === task.id}
                      className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200 disabled:bg-gray-100 disabled:text-gray-400 transition-colors"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(task.id)}
                      disabled={actionLoading === task.id}
                      className="px-3 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200 disabled:bg-gray-100 disabled:text-gray-400 transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
