# Todo App Frontend

This is the frontend implementation for the Todo App Phase II project, built with Next.js 16 and integrated with Better Auth for authentication.

## Features

- **Authentication**: Secure login and registration using Better Auth with JWT token handling
- **Task Management**: Create, read, update, and delete tasks with completion toggling
- **Responsive Design**: Mobile-friendly interface that works across all device sizes
- **Route Protection**: Protected routes that require authentication
- **Secure Token Handling**: Proper JWT token storage, refresh, and expiration handling
- **Error Handling**: Comprehensive error handling and user feedback

## Architecture

The frontend follows the requirements specified in the project constitution and spec files:

- Built with Next.js 16 using the App Router
- Uses Better Auth for authentication management
- Implements JWT token handling for secure communication with the backend
- Follows a component-based architecture with reusable UI components

## Key Components

- `lib/auth-client.ts`: Better Auth configuration
- `lib/token-utils.ts`: JWT token management utilities
- `lib/api-client.ts`: Backend API service with JWT interceptors
- `lib/types.ts`: TypeScript type definitions for API models
- `hooks/useTasks.ts`: Custom hook for task CRUD operations
- `components/tasks/TaskListComponent.tsx`: Component for displaying and managing tasks
- `components/tasks/TaskFormComponent.tsx`: Component for creating new tasks
- `components/tasks/TaskItemComponent.tsx`: Individual task item component
- `components/tasks/TaskFilter.tsx`: Filter buttons for task views
- `app/dashboard/page.tsx`: Protected dashboard page
- `app/login/page.tsx`: Login page
- `app/register/page.tsx`: Registration page

## Security Features

- JWT tokens stored securely in localStorage with expiration tracking
- Automatic token refresh handling
- Proper error handling for expired or invalid tokens
- Route protection preventing unauthorized access
- Input validation and sanitization

## API Integration

The frontend communicates with the backend through a centralized API client that:

- Attaches JWT tokens to all authenticated requests
- Handles token expiration and refresh
- Provides consistent error handling
- Implements proper session management

## Responsive Design

The UI is designed to be responsive and accessible:

- Mobile-first approach with responsive breakpoints
- Accessible markup with proper semantic HTML
- Support for reduced motion and high contrast modes
- Keyboard navigation support