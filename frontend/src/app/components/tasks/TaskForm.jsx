import { useState } from 'react';
import { taskService } from '../../services/taskService';

const TaskForm = ({ userId, onTaskCreated }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    due_date: '',
    priority: 'medium',
    assigned_class: ''
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      const newTask = await taskService.createTask({
        ...formData,
        user_id: userId
      });
      
      setFormData({
        title: '',
        description: '',
        category: '',
        due_date: '',
        priority: 'medium',
        assigned_class: ''
      });
      setError('');
      
      if (onTaskCreated) {
        onTaskCreated(newTask);
      }
    } catch (error) {
      setError('Failed to create task');
      console.error('Error creating task:', error);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Task</h3>
      
      {error && (
        <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-lg">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition duration-300"
            placeholder="Task title"
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={2}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition duration-300"
            placeholder="Task description"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition duration-300"
            >
              <option value="">Select category</option>
              <option value="lesson-planning">Lesson Planning</option>
              <option value="grading">Grading</option>
              <option value="meetings">Meetings</option>
              <option value="parent-communication">Parent Communication</option>
              <option value="professional-development">Professional Development</option>
            </select>
          </div>

          <div>
            <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition duration-300"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 mb-1">
              Due Date
            </label>
            <input
              type="date"
              id="due_date"
              name="due_date"
              value={formData.due_date}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition duration-300"
            />
          </div>

          <div>
            <label htmlFor="assigned_class" className="block text-sm font-medium text-gray-700 mb-1">
              Assigned Class
            </label>
            <input
              type="text"
              id="assigned_class"
              name="assigned_class"
              value={formData.assigned_class}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition duration-300"
              placeholder="Class name"
            />
          </div>
        </div>

        <button
          type="submit"
          className="w-full px-4 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition duration-300 font-medium"
        >
          Add Task
        </button>
      </form>
    </div>
  );
};

export default TaskForm;