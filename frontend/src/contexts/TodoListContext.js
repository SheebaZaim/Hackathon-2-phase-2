import { createContext, useContext, useReducer } from 'react';

// Define types
interface TodoList {
  id: string;
  title: string;
  description?: string;
  is_public: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
  position: number;
}

interface Task {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  todo_list_id: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
  position: number;
}

interface TodoListState {
  todoLists: TodoList[];
  tasks: Record<string, Task[]>; // Map of todoListId to tasks
  loading: boolean;
  error: string | null;
}

type TodoListAction =
  | { type: 'FETCH_TODO_LISTS_START' }
  | { type: 'FETCH_TODO_LISTS_SUCCESS'; payload: TodoList[] }
  | { type: 'FETCH_TODO_LISTS_ERROR'; payload: string }
  | { type: 'ADD_TODO_LIST'; payload: TodoList }
  | { type: 'UPDATE_TODO_LIST'; payload: TodoList }
  | { type: 'DELETE_TODO_LIST'; payload: string }
  | { type: 'FETCH_TASKS_START'; payload: string } // payload is todoListId
  | { type: 'FETCH_TASKS_SUCCESS'; payload: { todoListId: string; tasks: Task[] } }
  | { type: 'FETCH_TASKS_ERROR'; payload: { todoListId: string; error: string } }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: Task }
  | { type: 'DELETE_TASK'; payload: string } // payload is taskId
  | { type: 'TOGGLE_TASK_COMPLETION'; payload: Task };

const TodoListContext = createContext<{
  state: TodoListState;
  fetchTodoLists: () => Promise<void>;
  addTodoList: (todoListData: Omit<TodoList, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => Promise<void>;
  updateTodoList: (id: string, updates: Partial<TodoList>) => Promise<void>;
  deleteTodoList: (id: string) => Promise<void>;
  fetchTasks: (todoListId: string) => Promise<void>;
  addTask: (todoListId: string, taskData: Omit<Task, 'id' | 'todo_list_id' | 'created_at' | 'updated_at'>) => Promise<void>;
  updateTask: (taskId: string, updates: Partial<Task>) => Promise<void>;
  deleteTask: (taskId: string) => Promise<void>;
  toggleTaskCompletion: (taskId: string) => Promise<void>;
} | undefined>(undefined);

const todoListReducer = (state: TodoListState, action: TodoListAction): TodoListState => {
  switch (action.type) {
    case 'FETCH_TODO_LISTS_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_TODO_LISTS_SUCCESS':
      return { ...state, loading: false, todoLists: action.payload };
    case 'FETCH_TODO_LISTS_ERROR':
      return { ...state, loading: false, error: action.payload };
    case 'ADD_TODO_LIST':
      return { ...state, todoLists: [...state.todoLists, action.payload] };
    case 'UPDATE_TODO_LIST':
      return {
        ...state,
        todoLists: state.todoLists.map(list =>
          list.id === action.payload.id ? action.payload : list
        ),
      };
    case 'DELETE_TODO_LIST':
      // Remove the todo list
      const updatedLists = state.todoLists.filter(list => list.id !== action.payload);
      // Also remove the associated tasks
      const updatedTasks = { ...state.tasks };
      delete updatedTasks[action.payload];
      return { ...state, todoLists: updatedLists, tasks: updatedTasks };
    case 'FETCH_TASKS_START':
      return state;
    case 'FETCH_TASKS_SUCCESS':
      return {
        ...state,
        tasks: {
          ...state.tasks,
          [action.payload.todoListId]: action.payload.tasks,
        },
      };
    case 'FETCH_TASKS_ERROR':
      return { ...state, error: action.payload.error };
    case 'ADD_TASK':
      return {
        ...state,
        tasks: {
          ...state.tasks,
          [action.payload.todo_list_id]: [
            ...(state.tasks[action.payload.todo_list_id] || []),
            action.payload,
          ],
        },
      };
    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: {
          ...state.tasks,
          [action.payload.todo_list_id]: (state.tasks[action.payload.todo_list_id] || []).map(task =>
            task.id === action.payload.id ? action.payload : task
          ),
        },
      };
    case 'DELETE_TASK':
      // Find the todo list ID for this task
      let todoListIdForTask = '';
      for (const [listId, tasks] of Object.entries(state.tasks)) {
        if (tasks.some(task => task.id === action.payload)) {
          todoListIdForTask = listId;
          break;
        }
      }
      
      if (todoListIdForTask) {
        return {
          ...state,
          tasks: {
            ...state.tasks,
            [todoListIdForTask]: state.tasks[todoListIdForTask].filter(task => task.id !== action.payload),
          },
        };
      }
      return state;
    case 'TOGGLE_TASK_COMPLETION':
      return {
        ...state,
        tasks: {
          ...state.tasks,
          [action.payload.todo_list_id]: (state.tasks[action.payload.todo_list_id] || []).map(task =>
            task.id === action.payload.id ? action.payload : task
          ),
        },
      };
    default:
      return state;
  }
};

export const TodoListProvider = ({ children }) => {
  const [state, dispatch] = useReducer(todoListReducer, {
    todoLists: [],
    tasks: {},
    loading: false,
    error: null,
  });

  const fetchTodoLists = async () => {
    dispatch({ type: 'FETCH_TODO_LISTS_START' });
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch('/api/v1/todo-lists/', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        dispatch({ type: 'FETCH_TODO_LISTS_SUCCESS', payload: data.data });
      } else {
        const errorData = await response.json();
        dispatch({ type: 'FETCH_TODO_LISTS_ERROR', payload: errorData.detail || 'Failed to fetch todo lists' });
      }
    } catch (error) {
      dispatch({ type: 'FETCH_TODO_LISTS_ERROR', payload: error.message || 'Network error' });
    }
  };

  const addTodoList = async (todoListData) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch('/api/v1/todo-lists/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(todoListData),
      });

      if (response.ok) {
        const data = await response.json();
        dispatch({ type: 'ADD_TODO_LIST', payload: data.data });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to add todo list');
      }
    } catch (error) {
      throw error;
    }
  };

  const updateTodoList = async (id, updates) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch(`/api/v1/todo-lists/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(updates),
      });

      if (response.ok) {
        const data = await response.json();
        dispatch({ type: 'UPDATE_TODO_LIST', payload: data.data });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update todo list');
      }
    } catch (error) {
      throw error;
    }
  };

  const deleteTodoList = async (id) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch(`/api/v1/todo-lists/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        dispatch({ type: 'DELETE_TODO_LIST', payload: id });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete todo list');
      }
    } catch (error) {
      throw error;
    }
  };

  const fetchTasks = async (todoListId) => {
    dispatch({ type: 'FETCH_TASKS_START', payload: todoListId });
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch(`/api/v1/tasks/todo-lists/${todoListId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        dispatch({ type: 'FETCH_TASKS_SUCCESS', payload: { todoListId, tasks: data.data } });
      } else {
        const errorData = await response.json();
        dispatch({ type: 'FETCH_TASKS_ERROR', payload: { todoListId, error: errorData.detail || 'Failed to fetch tasks' } });
      }
    } catch (error) {
      dispatch({ type: 'FETCH_TASKS_ERROR', payload: { todoListId, error: error.message || 'Network error' } });
    }
  };

  const addTask = async (todoListId, taskData) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch(`/api/v1/tasks/todo-lists/${todoListId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(taskData),
      });

      if (response.ok) {
        const data = await response.json();
        dispatch({ type: 'ADD_TASK', payload: data.data });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to add task');
      }
    } catch (error) {
      throw error;
    }
  };

  const updateTask = async (taskId, updates) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch(`/api/v1/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(updates),
      });

      if (response.ok) {
        const data = await response.json();
        dispatch({ type: 'UPDATE_TASK', payload: data.data });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update task');
      }
    } catch (error) {
      throw error;
    }
  };

  const deleteTask = async (taskId) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch(`/api/v1/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        dispatch({ type: 'DELETE_TASK', payload: taskId });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete task');
      }
    } catch (error) {
      throw error;
    }
  };

  const toggleTaskCompletion = async (taskId) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await fetch(`/api/v1/tasks/${taskId}/toggle-completion`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        dispatch({ type: 'TOGGLE_TASK_COMPLETION', payload: data.data });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to toggle task completion');
      }
    } catch (error) {
      throw error;
    }
  };

  const value = {
    state,
    fetchTodoLists,
    addTodoList,
    updateTodoList,
    deleteTodoList,
    fetchTasks,
    addTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };

  return (
    <TodoListContext.Provider value={value}>
      {children}
    </TodoListContext.Provider>
  );
};

export const useTodoList = () => {
  const context = useContext(TodoListContext);
  if (!context) {
    throw new Error('useTodoList must be used within a TodoListProvider');
  }
  return context;
};