import { useState } from 'react';
import { useTodoList } from '../../contexts/TodoListContext';

const TodoListForm = ({ onCancel }) => {
  const { addTodoList } = useTodoList();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isPublic, setIsPublic] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      alert('Todo list title is required');
      return;
    }

    try {
      await addTodoList({
        title,
        description,
        is_public: isPublic,
        position: 0,
      });
      
      // Reset form
      setTitle('');
      setDescription('');
      setIsPublic(false);
      
      // Optionally notify parent component
      if (onCancel) onCancel();
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <h3 className="font-medium text-lg mb-3">Create New Todo List</h3>
      
      <div className="mb-3">
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="List title"
          required
        />
      </div>
      
      <div className="mb-3">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="List description (optional)"
          rows="2"
        />
      </div>
      
      <div className="mb-4 flex items-center">
        <input
          type="checkbox"
          id="isPublic"
          checked={isPublic}
          onChange={(e) => setIsPublic(e.target.checked)}
          className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
        />
        <label htmlFor="isPublic" className="ml-2 block text-sm text-gray-700">
          Make this list public
        </label>
      </div>
      
      <div className="flex space-x-2">
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Create List
        </button>
        
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default TodoListForm;