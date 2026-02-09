// components/tasks/TaskForm.jsx
'use client';

import { useState } from 'react';
import { taskAPI } from '../../app/api/task_api';
import { useNotifications } from '../../contexts/NotificationContext';

const TaskForm = ({ userId, onTaskCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [category, setCategory] = useState('work');
  const [priority, setPriority] = useState('medium');
  const [loading, setLoading] = useState(false);
  const { success, error: showError } = useNotifications();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      showError('Title is required');
      return;
    }

    setLoading(true);
    
    try {
      const taskData = {
        title: title.trim(),
        description: description.trim(),
        due_date: dueDate || new Date().toISOString(),
        category,
        priority
      };
      
      const newTask = await taskAPI.createTask(taskData);
      success('Task created successfully!');
      
      // Reset form
      setTitle('');
      setDescription('');
      setDueDate('');
      setCategory('work');
      setPriority('medium');
      
      if (onTaskCreated) {
        onTaskCreated(newTask);
      }
    } catch (err) {
      showError(`Failed to create task: ${err.message}`);
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow-lg rounded-2xl overflow-hidden border border-gray-100 transition-all duration-300 hover:shadow-xl">
      <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100 rounded-t-2xl">
        <h3 className="text-lg leading-6 font-medium text-gray-900">Create New Task</h3>
        <p className="mt-1 text-sm text-gray-500">Add a new task to your list</p>
      </div>
      <div className="p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="block w-full px-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200 shadow-sm bg-white"
              placeholder="Task title"
              required
            />
          </div>
          
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="block w-full px-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200 shadow-sm bg-white"
              rows="3"
              placeholder="Task description"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-1">
                Due Date
              </label>
              <input
                type="date"
                id="dueDate"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="block w-full px-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200 shadow-sm bg-white"
              />
            </div>
            
            <div>
              <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                id="priority"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="block w-full px-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200 shadow-sm bg-white"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
          
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              id="category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="block w-full px-4 py-3.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition duration-200 shadow-sm bg-white"
            >
              <option value="work">Work</option>
              <option value="personal">Personal</option>
              <option value="education">Education</option>
              <option value="meeting">Meeting</option>
              <option value="assignment">Assignment</option>
              <option value="grading">Grading</option>
              <option value="planning">Planning</option>
            </select>
          </div>
          
          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className={`w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200 shadow-md hover:shadow-lg font-medium py-3.5 px-6 ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
            >
              {loading ? 'Creating...' : 'Create Task'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TaskForm;