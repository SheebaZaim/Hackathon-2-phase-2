# Quickstart Guide: Run Frontend and Backend

## Overview
This guide provides instructions for setting up and running both frontend and backend applications simultaneously using the orchestration tools.

## Prerequisites
- Node.js v16+ installed
- npm or yarn package manager
- Both frontend and backend applications already set up and functional separately
- Available ports (default: frontend on 3000, backend on 8000)

## Setup Instructions

### 1. Clone/Access the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Navigate to the Feature Branch
```bash
git checkout 004-run-frontend-backend
```

## Configuration

### 1. Set Up Environment Configuration
Create or update configuration files in the `config/` directory:

```
config/
├── dev/
│   ├── frontend.config.json
│   ├── backend.config.json
│   └── orchestration.config.json
├── staging/
│   ├── frontend.config.json
│   ├── backend.config.json
│   └── orchestration.config.json
└── production/
    ├── frontend.config.json
    ├── backend.config.json
    └── orchestration.config.json
```

### 2. Example Configuration Files

#### orchestration.config.json
```json
{
  "frontend": {
    "port": 3000,
    "host": "localhost",
    "command": "npm run dev",
    "env": {
      "REACT_APP_API_URL": "http://localhost:8000/api"
    }
  },
  "backend": {
    "port": 8000,
    "host": "localhost",
    "command": "npm run start:dev",
    "env": {
      "PORT": 8000
    }
  },
  "communication": {
    "proxyUrl": "http://localhost:8000",
    "corsOrigins": ["http://localhost:3000"]
  },
  "startup": {
    "waitForBackend": true,
    "timeout": 30000
  },
  "shutdown": {
    "gracefulTimeout": 5000
  }
}
```

## Running Applications

### 1. Using Package Scripts (Recommended)
```bash
# Start both applications
npm run dev

# Or using yarn
yarn dev
```

### 2. Using Direct Scripts
```bash
# Start both applications using the orchestration script
node scripts/start-dev.js

# Stop both applications
node scripts/stop-dev.js
```

### 3. Using Docker (Optional)
```bash
# If Docker is configured
docker-compose up
```

## Verification

### 1. Check Application Status
```bash
# Run health check
node scripts/health-check.js
```

### 2. Verify Communication
- Access the frontend at `http://localhost:3000`
- Verify API calls to the backend are working
- Check that CORS headers are properly set

### 3. View Logs
- Frontend logs will appear in the terminal
- Backend logs will appear in the terminal
- Additional logs may be available in `logs/` directory

## Troubleshooting

### Common Issues

#### Port Already in Use
- Check if applications are already running
- Modify ports in configuration files
- Kill existing processes using the ports

#### CORS Errors
- Verify CORS settings in backend configuration
- Ensure frontend URL is in the allowed origins list

#### Environment Variables Not Loaded
- Check that configuration files are properly formatted
- Verify that environment variables are correctly set

### Debugging Commands
```bash
# Check if ports are available
netstat -an | grep :3000
netstat -an | grep :8000

# Check running processes
ps aux | grep -E "(node|npm|yarn)"

# Force kill processes if needed
pkill -f "node.*frontend"
pkill -f "node.*backend"
```

## Stopping Applications

### 1. Graceful Shutdown
- Press `Ctrl+C` in the terminal where applications are running
- The orchestration script will handle graceful shutdown

### 2. Manual Shutdown
```bash
# Stop applications using script
node scripts/stop-dev.js

# Or use package script
npm run dev:stop
```

## Customization

### Changing Port Numbers
Update the `orchestration.config.json` file:
```json
{
  "frontend": {
    "port": 3001,  // Changed from default 3000
    ...
  },
  "backend": {
    "port": 8001,  // Changed from default 8000
    ...
  }
}
```

### Adding Environment Variables
Add to the `env` sections in configuration files:
```json
{
  "frontend": {
    "env": {
      "REACT_APP_NEW_VAR": "value",
      ...
    }
  },
  "backend": {
    "env": {
      "NEW_BACKEND_VAR": "value",
      ...
    }
  }
}
```