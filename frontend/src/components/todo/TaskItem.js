import { useState, useEffect } from 'react';
import { useTodoList } from '../../contexts/TodoListContext';

const TaskItem = ({ todoListId }) => {
  const { state, addTask, updateTask, deleteTask, toggleTaskCompletion } = useTodoList();
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState('medium');
  const [showForm, setShowForm] = useState(false);

  // Get tasks for this specific todo list
  const tasks = state.tasks[todoListId] || [];

  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      await addTask(todoListId, {
        title: newTaskTitle,
        description: newTaskDescription,
        priority: newTaskPriority,
      });
      setNewTaskTitle('');
      setNewTaskDescription('');
      setNewTaskPriority('medium');
      setShowForm(false);
    } catch (error) {
      alert(error.message);
    }
  };

  const handleToggleCompletion = async (task) => {
    try {
      await toggleTaskCompletion(task.id);
    } catch (error) {
      alert(error.message);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(taskId);
      } catch (error) {
        alert(error.message);
      }
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h4 className="font-medium text-gray-800">Tasks</h4>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 text-sm"
        >
          {showForm ? 'Cancel' : '+ Add Task'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleAddTask} className="mb-4 p-3 bg-gray-50 rounded">
          <div className="mb-2">
            <input
              type="text"
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              placeholder="Task title"
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
              required
            />
          </div>
          <div className="mb-2">
            <textarea
              value={newTaskDescription}
              onChange={(e) => setNewTaskDescription(e.target.value)}
              placeholder="Task description (optional)"
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
              rows="2"
            />
          </div>
          <div className="mb-3">
            <select
              value={newTaskPriority}
              onChange={(e) => setNewTaskPriority(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="low">Low Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="high">High Priority</option>
            </select>
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Add Task
          </button>
        </form>
      )}

      {tasks.length === 0 ? (
        <p className="text-gray-500 italic">No tasks yet. Add one above!</p>
      ) : (
        <ul className="space-y-2">
          {tasks.map((task) => (
            <li key={task.id} className="p-3 bg-white border rounded flex justify-between items-start">
              <div className="flex items-start">
                <input
                  type="checkbox"
                  checked={task.is_completed}
                  onChange={() => handleToggleCompletion(task)}
                  className="mt-1 mr-2"
                />
                <div>
                  <div className={`font-medium ${task.is_completed ? 'line-through text-gray-500' : ''}`}>
                    {task.title}
                  </div>
                  {task.description && (
                    <div className="text-sm text-gray-600 mt-1">{task.description}</div>
                  )}
                  <div className="text-xs mt-1">
                    <span className={`px-2 py-1 rounded-full ${
                      task.priority === 'high' ? 'bg-red-100 text-red-800' :
                      task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)} priority
                    </span>
                    {task.due_date && (
                      <span className="ml-2 text-gray-500">
                        Due: {new Date(task.due_date).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
              </div>
              <button
                onClick={() => handleDeleteTask(task.id)}
                className="text-red-500 hover:text-red-700 text-sm"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskItem;