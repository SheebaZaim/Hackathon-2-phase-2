import { useState, useEffect } from 'react';
import { useTodoList } from '../contexts/TodoListContext';
import { useAuth } from '../contexts/AuthContext';
import TodoListCard from '../components/todo/TodoListCard';
import ProtectedRoute from '../components/auth/ProtectedRoute';

const TodoListsPage = () => {
  const { state, fetchTodoLists, addTodoList } = useTodoList();
  const { user } = useAuth();
  const [newListTitle, setNewListTitle] = useState('');
  const [newListDescription, setNewListDescription] = useState('');
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    if (user) {
      fetchTodoLists();
    }
  }, [user]);

  const handleAddList = async (e) => {
    e.preventDefault();
    if (!newListTitle.trim()) return;

    try {
      await addTodoList({
        title: newListTitle,
        description: newListDescription,
        is_public: false,
        position: 0,
      });
      setNewListTitle('');
      setNewListDescription('');
      setShowForm(false);
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <ProtectedRoute>
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">My Todo Lists</h1>
        
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Your Lists</h2>
            <button
              onClick={() => setShowForm(!showForm)}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {showForm ? 'Cancel' : '+ New List'}
            </button>
          </div>

          {showForm && (
            <form onSubmit={handleAddList} className="mb-6 p-4 bg-gray-50 rounded-lg">
              <div className="mb-3">
                <input
                  type="text"
                  value={newListTitle}
                  onChange={(e) => setNewListTitle(e.target.value)}
                  placeholder="List title"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="mb-3">
                <textarea
                  value={newListDescription}
                  onChange={(e) => setNewListDescription(e.target.value)}
                  placeholder="List description (optional)"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows="2"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
              >
                Create List
              </button>
            </form>
          )}

          {state.loading ? (
            <div className="text-center py-8">
              <p>Loading your todo lists...</p>
            </div>
          ) : state.error ? (
            <div className="p-4 bg-red-100 text-red-700 rounded">
              Error: {state.error}
            </div>
          ) : state.todoLists.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-600">You don't have any todo lists yet.</p>
              <p className="text-gray-500 mt-2">Create your first list to get started!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {state.todoLists.map((todoList) => (
                <TodoListCard key={todoList.id} todoList={todoList} />
              ))}
            </div>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default TodoListsPage;