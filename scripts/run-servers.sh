#!/bin/bash

# Script to run both frontend and backend servers according to constitution requirements

echo "Starting Professional Todo App Servers..."
echo "========================================="

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "Error: backend directory not found!"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "Error: frontend directory not found!"
    exit 1
fi

echo "Starting Backend Server (FastAPI)..."
echo "------------------------------------"

# Start backend server in background
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "Starting Frontend Server (Next.js)..."
echo "-------------------------------------"

# Start frontend server in background
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Both servers are now running..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"

echo ""
echo "Press Ctrl+C to stop both servers..."

# Trap SIGINT and SIGTERM to properly kill background processes
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID