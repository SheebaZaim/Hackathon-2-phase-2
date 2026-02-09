// Task Form Component

'use client';

import React, { useState } from 'react';
import { taskAPI } from '../api/task_api';

const TaskForm = ({ onTaskCreated, userId }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.trim().length > 255) {
      setError('Title must be 255 characters or less');
      return;
    }

    if (description.length > 1000) {
      setError('Description must be 1000 characters or less');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const newTask = await taskAPI.createTask({
        title: title.trim(),
        description: description.trim()
      });

      // Reset form
      setTitle('');
      setDescription('');
      setError(null);

      if (onTaskCreated) {
        onTaskCreated(newTask);
      }
    } catch (err) {
      setError('Failed to create task. Please try again.');
      console.error('Error creating task:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg overflow-hidden mb-6">
      <h2 className="text-xl font-semibold p-4 border-b">Create New Task</h2>
      <form onSubmit={handleSubmit} className="p-4">
        {error && (
          <div className="mb-4 text-red-500 bg-red-50 p-2 rounded">
            {error}
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter task title"
            maxLength={255}
          />
        </div>

        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter task description (optional)"
            rows="3"
            maxLength={1000}
          />
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Creating...' : 'Create Task'}
        </button>
      </form>
    </div>
  );
};

export default TaskForm;