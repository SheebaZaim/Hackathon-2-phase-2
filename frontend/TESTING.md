# Todo App Frontend - Testing Guide

## Prerequisites

1. **Backend running**: The backend must be running at `http://localhost:8000`
   ```bash
   cd backend
   backend_env_py311/Scripts/python.exe -m uvicorn src.main:app --reload
   ```

2. **Environment variables**: Create `.env.local` from `.env.example`
   ```bash
   cp .env.example .env.local
   ```

3. **Backend health check**: Verify backend is accessible
   ```bash
   curl http://localhost:8000/health
   ```
   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2026-02-10T...",
     "database": "connected"
   }
   ```

## Setup Steps

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment variables** in `.env.local`:
   ```env
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   NEXT_PUBLIC_API_URL=http://localhost:3000
   BETTER_AUTH_SECRET=<copy-from-backend-env>
   BETTER_AUTH_URL=http://localhost:3000
   DATABASE_URL=<copy-from-backend-env>
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open browser**: Navigate to `http://localhost:3000`

## Manual Testing Checklist

### 1. Health Check & Backend Connection
- [ ] Backend is running and accessible at `http://localhost:8000`
- [ ] Frontend loads at `http://localhost:3000`
- [ ] No console errors on homepage

### 2. Homepage
- [ ] Homepage displays correctly
- [ ] "Get Started" and "Sign In" buttons are visible
- [ ] Features section displays three feature cards
- [ ] Responsive design works on mobile/tablet/desktop

### 3. User Registration
- [ ] Navigate to `/register`
- [ ] Fill in email and password
- [ ] Submit form
- [ ] Check for validation errors with invalid input:
  - [ ] Password < 8 characters shows error
  - [ ] Passwords don't match shows error
  - [ ] Invalid email format shows error
- [ ] Successful registration redirects to dashboard
- [ ] User is automatically logged in

### 4. User Login
- [ ] Navigate to `/login`
- [ ] Enter valid credentials
- [ ] Submit form
- [ ] Successful login redirects to dashboard
- [ ] Invalid credentials show error message
- [ ] Token is stored in localStorage

### 5. Dashboard Access
- [ ] Dashboard loads at `/dashboard`
- [ ] User email is displayed in header
- [ ] Logout button is visible
- [ ] Task form is displayed
- [ ] Filter buttons (All, Active, Completed) are visible
- [ ] Empty state shows when no tasks exist

### 6. Task Creation
- [ ] Enter task title in form
- [ ] Click "Add" button
- [ ] Task appears in list immediately
- [ ] Task is saved to backend (verify by refreshing page)
- [ ] Empty title shows validation error
- [ ] Very long title (>500 chars) shows error
- [ ] Input is cleared after successful submission

### 7. Task Display
- [ ] Tasks display with correct title
- [ ] Checkbox is unchecked for new tasks
- [ ] Created timestamp is displayed
- [ ] Edit and Delete buttons are visible
- [ ] Tasks are sorted correctly (newest first or by creation date)

### 8. Task Completion Toggle
- [ ] Click checkbox on active task
- [ ] Task title gets strikethrough
- [ ] Task is marked as completed in backend
- [ ] Click checkbox on completed task
- [ ] Strikethrough is removed
- [ ] Task is marked as active in backend

### 9. Task Editing
- [ ] Click "Edit" button on a task
- [ ] Input field appears with current title
- [ ] Modify title
- [ ] Press Enter or click "Save"
- [ ] Task title updates immediately
- [ ] Updated title is saved to backend
- [ ] Press Escape or click "Cancel" to abort edit
- [ ] Empty title during edit shows error

### 10. Task Deletion
- [ ] Click "Delete" button on a task
- [ ] Confirmation dialog appears
- [ ] Click "OK" to confirm
- [ ] Task is removed from list
- [ ] Task is deleted from backend (verify by refresh)
- [ ] Click "Cancel" to abort deletion

### 11. Task Filtering
- [ ] Click "All" filter
  - [ ] All tasks are displayed (active + completed)
- [ ] Click "Active" filter
  - [ ] Only uncompleted tasks are shown
  - [ ] Completed tasks are hidden
- [ ] Click "Completed" filter
  - [ ] Only completed tasks are shown
  - [ ] Active tasks are hidden
- [ ] Create new task while on "Active" filter
  - [ ] New task appears in list
- [ ] Toggle task completion while on filtered view
  - [ ] Task moves to correct filter category

### 12. User Isolation
- [ ] Logout from first user account
- [ ] Register a second user
- [ ] Login with second user
- [ ] Create tasks for second user
- [ ] Verify second user cannot see first user's tasks
- [ ] Logout from second user
- [ ] Login with first user
- [ ] Verify first user's tasks are still intact
- [ ] Verify first user cannot see second user's tasks

### 13. Session Management
- [ ] Login to account
- [ ] Navigate to dashboard
- [ ] Close browser tab
- [ ] Reopen browser and navigate to `/dashboard`
- [ ] Verify user is still logged in (session persisted)
- [ ] Click Logout
- [ ] Verify redirect to homepage
- [ ] Try to access `/dashboard` directly
- [ ] Verify redirect to `/login`

### 14. Error Handling
- [ ] Stop backend server
- [ ] Try to create a task
- [ ] Verify error message is displayed
- [ ] Start backend server
- [ ] Verify tasks load correctly
- [ ] Simulate network error (browser DevTools)
- [ ] Verify graceful error handling

### 15. Responsive Design
- [ ] Test on mobile viewport (320px width)
  - [ ] All elements are accessible
  - [ ] No horizontal scrolling
  - [ ] Buttons are tap-friendly
- [ ] Test on tablet viewport (768px width)
  - [ ] Layout adjusts appropriately
- [ ] Test on desktop viewport (1920px width)
  - [ ] Layout uses available space well
  - [ ] Max-width container is applied

### 16. Authentication Edge Cases
- [ ] Expired token handling
  - [ ] Wait for token to expire (if applicable)
  - [ ] Make API request
  - [ ] Verify redirect to login
- [ ] Invalid token
  - [ ] Manually modify token in localStorage
  - [ ] Reload page
  - [ ] Verify redirect to login
- [ ] Concurrent sessions
  - [ ] Login on two different browsers
  - [ ] Create tasks in both
  - [ ] Verify both sessions work independently

### 17. Performance
- [ ] Load dashboard with 50+ tasks
- [ ] Verify smooth scrolling
- [ ] Verify quick task toggle response
- [ ] Check for memory leaks (browser DevTools)

### 18. Accessibility
- [ ] Navigate using keyboard only
  - [ ] Tab through form fields
  - [ ] Use Enter to submit forms
  - [ ] Use Space to toggle checkboxes
- [ ] Test with screen reader (if available)
- [ ] Verify color contrast is sufficient
- [ ] Check focus indicators are visible

## Known Issues & Limitations

- **Better Auth Integration**: The current implementation uses Better Auth client-side. Full server-side integration with the backend JWT may require additional configuration.
- **Token Refresh**: Automatic token refresh is not yet implemented. Users will need to re-login when tokens expire.
- **Real-time Updates**: The app does not have WebSocket support. Changes by other users won't appear without manual refresh.

## Troubleshooting

### Frontend won't start
- Check Node.js version (should be 18+)
- Delete `node_modules` and `package-lock.json`, then run `npm install`
- Check for port conflicts on 3000

### Backend connection errors
- Verify backend is running on port 8000
- Check CORS configuration in backend allows `http://localhost:3000`
- Verify `NEXT_PUBLIC_BACKEND_URL` in `.env.local`

### Authentication not working
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check `DATABASE_URL` is correct
- Clear localStorage and cookies, then try again
- Check browser console for errors

### Tasks not loading
- Open browser DevTools Network tab
- Check API requests to `http://localhost:8000/api/tasks`
- Verify Authorization header is present
- Check backend logs for errors

### TypeScript errors
- Run `npm run build` to check for type errors
- Ensure all dependencies are installed
- Check `tsconfig.json` configuration

## Browser Console Checks

During testing, monitor the browser console for:
- ✅ No red errors (except expected validation errors)
- ✅ API requests show 200/201 status codes
- ✅ JWT tokens are included in Authorization headers
- ✅ No CORS errors

## Success Criteria

All 18 test sections should pass without errors for the frontend to be considered production-ready.

## Next Steps After Testing

1. Fix any identified bugs
2. Implement token refresh if needed
3. Add loading skeletons for better UX
4. Implement toast notifications for user feedback
5. Add unit and integration tests
6. Deploy to Vercel or similar platform
7. Configure production environment variables
