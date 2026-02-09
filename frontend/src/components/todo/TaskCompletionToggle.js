import { useTodoList } from '../contexts/TodoListContext';

const TaskCompletionToggle = ({ task }) => {
  const { toggleTaskCompletion } = useTodoList();

  const handleToggle = async () => {
    try {
      await toggleTaskCompletion(task.id);
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <button
      onClick={handleToggle}
      className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
        task.is_completed
          ? 'bg-green-500 border-green-500 text-white'
          : 'border-gray-300 hover:border-green-400'
      }`}
      aria-label={task.is_completed ? 'Mark as incomplete' : 'Mark as complete'}
    >
      {task.is_completed && (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
        </svg>
      )}
    </button>
  );
};

export default TaskCompletionToggle;