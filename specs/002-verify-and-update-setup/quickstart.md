# Quickstart Guide: Verify and Update Setup

**Feature**: 002-verify-and-update-setup
**Date**: 2026-02-07

## Overview

This guide will help you quickly set up and run the verification process to identify missing components and ensure your frontend and backend run without errors.

## Prerequisites

- Node.js (v18 or higher)
- npm (v8 or higher)
- Python (v3.11 or higher)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Backend Dependencies

```bash
cd backend
npm install
cd ..
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Set Up Environment Variables

Create `.env` files in both `backend/` and `frontend/` directories:

Backend `.env`:
```env
NODE_ENV=development
PORT=3001
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
JWT_SECRET=your_jwt_secret
```

Frontend `.env`:
```env
REACT_APP_API_URL=http://localhost:3001
REACT_APP_ENVIRONMENT=development
```

## Running the Verification Process

### 1. Start the Backend Server

```bash
cd backend
npm run dev
```

### 2. In a new terminal, start the Frontend Server

```bash
cd frontend
npm run dev
```

### 3. Run Verification Scripts

To run the verification process that checks for missing components:

```bash
# From the project root
npm run verify-setup
```

Or run individual checks:

```bash
# Check backend health
npm run verify-backend

# Check frontend health
npm run verify-frontend

# Check integration
npm run verify-integration
```

## Running Tests

### Backend Tests

```bash
cd backend
npm test
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Full Integration Tests

```bash
npm run test-integration
```

## Common Issues and Solutions

### Issue: Port Already in Use
**Solution**: Change the PORT value in your backend `.env` file to an available port.

### Issue: Database Connection Error
**Solution**: Verify your database credentials in the backend `.env` file and ensure your database server is running.

### Issue: API Calls Failing
**Solution**: Check that your `REACT_APP_API_URL` in the frontend `.env` file matches your backend server URL.

## Next Steps

1. Review the verification report generated in `reports/verification-[timestamp].json`
2. Address any missing components listed in the report
3. Re-run verification after implementing changes
4. Ensure all tests pass before deploying

## Useful Commands

- `npm run build` - Build both frontend and backend for production
- `npm run lint` - Lint all code files
- `npm run verify-compliance` - Check constitution compliance
- `npm run start-all` - Start both frontend and backend servers
- `npm run test-all` - Run all tests (backend, frontend, integration)