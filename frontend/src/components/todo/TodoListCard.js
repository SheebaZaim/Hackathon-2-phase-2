import { useState } from 'react';
import { useTodoList } from '../contexts/TodoListContext';
import TaskItem from './TaskItem';

const TodoListCard = ({ todoList }) => {
  const { fetchTasks, deleteTodoList } = useTodoList();
  const [showTasks, setShowTasks] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleViewTasks = async () => {
    if (!showTasks) {
      setIsLoading(true);
      await fetchTasks(todoList.id);
      setIsLoading(false);
    }
    setShowTasks(!showTasks);
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${todoList.title}"?`)) {
      await deleteTodoList(todoList.id);
    }
  };

  return (
    <div className="border rounded-lg shadow-sm overflow-hidden">
      <div className="p-4 bg-gray-50 flex justify-between items-center">
        <div>
          <h3 className="font-semibold text-lg">{todoList.title}</h3>
          {todoList.description && (
            <p className="text-gray-600 text-sm mt-1">{todoList.description}</p>
          )}
        </div>
        <div className="flex space-x-2">
          <button
            onClick={handleViewTasks}
            className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
          >
            {showTasks ? 'Hide Tasks' : 'View Tasks'}
          </button>
          <button
            onClick={handleDelete}
            className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
          >
            Delete
          </button>
        </div>
      </div>
      
      {showTasks && (
        <div className="p-4">
          {isLoading ? (
            <p>Loading tasks...</p>
          ) : (
            <TaskItem todoListId={todoList.id} />
          )}
        </div>
      )}
    </div>
  );
};

export default TodoListCard;