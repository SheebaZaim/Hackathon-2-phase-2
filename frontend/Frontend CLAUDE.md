# Frontend Guidelines - Todo App

## Stack
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- Better Auth 1.5.0-beta.13
- Axios for HTTP requests

## Architecture

### Authentication Flow
1. **Better Auth** handles user registration and login
2. **JWT Tokens** are extracted from Better Auth session
3. **Token Storage** in localStorage for backend API calls
4. **API Client** automatically attaches tokens to requests

### Backend Integration
- Backend URL: `http://localhost:8000`
- All API calls go through `lib/api-client.ts`
- JWT tokens sent in `Authorization: Bearer <token>` header
- Automatic 401 handling → redirect to login

## Project Structure

```
src/
├── app/
│   ├── dashboard/page.tsx      # Protected dashboard page
│   ├── login/page.tsx          # Login page
│   ├── register/page.tsx       # Registration page
│   ├── layout.tsx              # Root layout
│   └── page.tsx                # Homepage
├── components/
│   └── tasks/
│       ├── TaskListComponent.tsx
│       ├── TaskItemComponent.tsx
│       ├── TaskFormComponent.tsx
│       └── TaskFilter.tsx
├── hooks/
│   └── useTasks.ts             # Task CRUD hook
├── lib/
│   ├── auth-client.ts          # Better Auth config
│   ├── token-utils.ts          # JWT utilities
│   ├── api-client.ts           # Backend API client
│   └── types.ts                # TypeScript types
└── styles/
    └── globals.css
```

## Patterns

### Client vs Server Components
- Use client components for interactivity ('use client')
- Dashboard, login, register are all client components
- Better Auth hooks require client components

### API Calls
All backend calls use the API client:

```typescript
import { taskAPI, healthAPI } from '@/lib/api-client';

// Health check
const status = await healthAPI.check();

// List tasks
const tasks = await taskAPI.list(); // All tasks
const activeTasks = await taskAPI.list(false); // Active only
const completedTasks = await taskAPI.list(true); // Completed only

// Create task
const newTask = await taskAPI.create('Task title');

// Update task
await taskAPI.update(taskId, { title: 'New title' });
await taskAPI.update(taskId, { completed: true });

// Delete task
await taskAPI.delete(taskId);
```

### Custom Hooks
Use `useTasks` hook for task management:

```typescript
import { useTasks } from '@/hooks/useTasks';

const { tasks, loading, error, createTask, updateTask, deleteTask, toggleTask, reload } = useTasks('all');
```

### Authentication
Better Auth integration:

```typescript
import { signIn, signUp, signOut, useSession } from '@/lib/auth-client';
import { setAuthToken, removeAuthToken } from '@/lib/token-utils';

// Sign in
const result = await signIn.email({ email, password });
if (result.data?.session?.token) {
  setAuthToken(result.data.session.token);
}

// Sign up
await signUp.email({ email, password, name });

// Sign out
await signOut();
removeAuthToken();

// Check session
const { data: session, isPending } = useSession();
```

## Styling
- Use Tailwind CSS classes
- No inline styles
- Follow existing component patterns
- Color scheme: Blue theme (blue-600, blue-700, etc.)
- Responsive design: mobile-first approach

## Type Safety
- All components use TypeScript
- Import types from `@/lib/types`
- Use proper type annotations for props and state

## Error Handling
- Show user-friendly error messages
- Handle network errors gracefully
- Validate user input before API calls
- Use try-catch for async operations

## Environment Variables
Required in `.env.local`:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:3000
BETTER_AUTH_SECRET=<same-as-backend>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=<neon-postgresql-url>
```

## Backend API Endpoints

The frontend integrates with these backend endpoints:

- `GET /health` - Health check
- `GET /api/tasks` - List tasks (with optional `completed` filter)
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

All task endpoints require JWT authentication.

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Testing

Manual testing checklist:
1. Register new user
2. Login with credentials
3. Create tasks
4. Toggle task completion
5. Edit task title
6. Delete tasks
7. Filter tasks (all/active/completed)
8. Logout
9. Verify user isolation (create second user)

## Notes

- Dashboard requires authentication
- Homepage redirects to dashboard if already logged in
- Tokens are stored in localStorage
- Backend must be running on port 8000
- Frontend runs on port 3000
