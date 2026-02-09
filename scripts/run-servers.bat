@echo off
REM Script to run both frontend and backend servers according to constitution requirements

echo Starting Professional Todo App Servers...
echo =========================================

REM Check if backend directory exists
if not exist "backend" (
    echo Error: backend directory not found!
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend" (
    echo Error: frontend directory not found!
    pause
    exit /b 1
)

echo Starting Backend Server (FastAPI)...
echo ------------------------------------

REM Start backend in a new window
start "Backend Server" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Starting Frontend Server (Next.js)...
echo -------------------------------------

REM Start frontend in a new window
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo Both servers should now be starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul