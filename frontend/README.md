# Todo App Frontend

This is the frontend implementation for the Todo App Phase II project, built with Next.js 14 and integrated with Better Auth for authentication.

## Features

- **Authentication**: Secure login and registration using Better Auth with JWT token handling
- **Task Management**: Create, read, update, and delete tasks with completion toggling
- **Responsive Design**: Mobile-friendly interface that works across all device sizes
- **Route Protection**: Protected routes that require authentication
- **Secure Token Handling**: Proper JWT token storage, refresh, and expiration handling
- **Error Handling**: Comprehensive error handling and user feedback

## Architecture

The frontend follows the requirements specified in the project constitution and spec files:

- Built with Next.js 14 using the App Router
- Uses Better Auth for authentication management
- Implements JWT token handling for secure communication with the backend
- Follows a component-based architecture with reusable UI components

## Key Components

- `auth.js`: Better Auth configuration and token management utilities
- `auth_api.js`: Authentication API service with JWT interceptors
- `task_api.js`: Task management API service with JWT interceptors
- `TaskList.jsx`: Component for displaying and managing user tasks
- `TaskForm.jsx`: Component for creating new tasks with validation
- `ProtectedRoute.jsx`: Higher-order component for route protection
- `AuthComponents.jsx`: Login and registration form components

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