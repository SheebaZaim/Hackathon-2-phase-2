import { useState, useEffect } from 'react';
import { taskService } from '../../services/taskService';
import EditModal from './EditModal';

const TaskList = ({ userId, onTaskUpdated }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingTask, setEditingTask] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await taskService.getAllTasks();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId) => {
    try {
      const updatedTask = await taskService.toggleTaskCompletion(taskId);
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const removeTask = async (taskId) => {
    try {
      await taskService.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  const handleEditClick = (task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleSaveTask = (updatedTask) => {
    setTasks(tasks.map(task => 
      task.id === updatedTask.id ? updatedTask : task
    ));
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingTask(null);
  };

  if (loading) {
    return <div className="text-center py-4">Loading tasks...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center py-4">{error}</div>;
  }

  return (
    <div className="bg-white rounded-lg overflow-hidden">
      {tasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No tasks yet. Create your first task!
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tasks.map((task) => (
            <div
              key={task.id}
              className={`border rounded-xl p-4 shadow-sm hover:shadow-lg transition-all duration-300 ${
                task.completed ? 'bg-gray-50 border-gray-200' : 'bg-white border-gray-200'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => toggleTaskCompletion(task.id)}
                    className="mt-1 h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
                  />
                  <div className="ml-3">
                    <h3
                      className={`font-medium ${
                        task.completed ? 'line-through text-gray-400' : 'text-gray-900'
                      }`}
                    >
                      {task.title}
                    </h3>
                    {task.description && (
                      <p className="mt-1 text-sm text-gray-600">{task.description}</p>
                    )}
                    {task.category && (
                      <span className="inline-block mt-2 px-2 py-1 text-xs font-medium bg-indigo-100 text-indigo-800 rounded-full">
                        {task.category.replace('-', ' ')}
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEditClick(task)}
                    className="text-indigo-600 hover:text-indigo-900"
                    title="Edit task"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => removeTask(task.id)}
                    className="text-red-600 hover:text-red-900"
                    title="Delete task"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>

              <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
                <span>{new Date(task.due_date).toLocaleDateString()}</span>
                <span className={`px-2 py-1 rounded-full ${
                  task.priority === 'high' ? 'bg-red-100 text-red-800' :
                  task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {task.priority}
                </span>
              </div>

              {task.assigned_class && (
                <div className="mt-2 text-xs text-indigo-600 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  {task.assigned_class}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
      {isModalOpen && editingTask && (
        <EditModal
          task={editingTask}
          isOpen={isModalOpen}
          onClose={closeModal}
          onSave={handleSaveTask}
        />
      )}
    </div>
  );
};

export default TaskList;