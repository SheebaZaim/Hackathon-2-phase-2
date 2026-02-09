// Task List Component

'use client';

import React, { useState, useEffect } from 'react';
import { taskAPI } from '../../app/api/task_api';
import { useNotifications } from '../../contexts/NotificationContext';

const TaskList = ({ userId }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const { success, error: showError } = useNotifications();

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await taskAPI.getTasks();
      setTasks(data);
    } catch (err) {
      showError('Failed to fetch tasks: ' + err.message);
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId) => {
    try {
      const updatedTask = await taskAPI.toggleTask(taskId);
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
      
      // Show success notification
      const taskTitle = tasks.find(t => t.id === taskId)?.title || 'Task';
      success(updatedTask.completed ? `${taskTitle} marked as completed` : `${taskTitle} marked as incomplete`);
    } catch (err) {
      showError('Failed to update task: ' + err.message);
      console.error('Error updating task:', err);
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await taskAPI.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
      
      // Show success notification
      const taskTitle = tasks.find(t => t.id === taskId)?.title || 'Task';
      success(`${taskTitle} deleted successfully`);
    } catch (err) {
      showError('Failed to delete task: ' + err.message);
      console.error('Error deleting task:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-lg rounded-2xl overflow-hidden border border-gray-100 transition-all duration-300 hover:shadow-xl w-full">
      <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100 rounded-t-2xl">
        <h2 className="text-xl font-semibold text-gray-800 flex items-center">
          <svg className="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
          Your Tasks
        </h2>
      </div>
      <div className="p-0">
        {tasks.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {tasks.map((task) => (
              <li key={task.id} className="border border-gray-200 rounded-2xl p-5 shadow-sm hover:shadow-lg transition-all duration-300 bg-white w-full hover-lift">
                <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => toggleTaskCompletion(task.id)}
                    className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500 border-gray-300 self-start sm:self-auto mt-1"
                  />
                  <div className="flex-1 min-w-0 w-full">
                    <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 sm:gap-0">
                      <h3 className={`text-lg font-medium ${
                        task.completed ? 'line-through text-gray-500' : 'text-gray-800'
                      }`}>
                        {task.title}
                      </h3>
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium shadow-sm ${
                        task.priority === 'high' ? 'bg-red-100 text-red-800 border border-red-200' :
                        task.priority === 'medium' ? 'bg-amber-100 text-amber-800 border border-amber-200' :
                        'bg-green-100 text-green-800 border border-green-200'
                      }`}>
                        {task.priority || 'medium'}
                      </span>
                    </div>
                    {task.description && (
                      <p className="mt-2 text-base text-gray-600 leading-relaxed">
                        {task.description}
                      </p>
                    )}
                    <div className="mt-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-0 text-sm text-gray-600">
                      <div className="flex items-center">
                        <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                      </div>
                      {task.due_date && (
                        <div className="flex items-center mt-1 sm:mt-0">
                          <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span>Due: {new Date(task.due_date).toLocaleDateString()}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => deleteTask(task.id)}
                    className="ml-0 sm:ml-4 inline-flex items-center p-2 border border-transparent rounded-full text-red-500 hover:text-red-700 hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-300 self-start sm:self-auto"
                    title="Delete task"
                  >
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default TaskList;