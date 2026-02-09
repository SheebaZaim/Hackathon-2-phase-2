# Data Model: Run Frontend and Backend

## Overview
This document outlines the configuration structures and data flows for the application orchestration feature. Since this is primarily a process orchestration feature, the "data model" focuses on configuration schemas and process state management.

## Configuration Structures

### Orchestration Configuration
- **Purpose**: Defines how the frontend and backend applications should be orchestrated
- **Schema**:
  - `frontend` (object): Frontend application configuration
    - `port` (number): Port number for the frontend application
    - `host` (string): Host address for the frontend application
    - `command` (string): Command to start the frontend application
    - `env` (object): Environment variables for the frontend
  - `backend` (object): Backend application configuration
    - `port` (number): Port number for the backend application
    - `host` (string): Host address for the backend application
    - `command` (string): Command to start the backend application
    - `env` (object): Environment variables for the backend
  - `communication` (object): Configuration for frontend-backend communication
    - `proxyUrl` (string): URL for backend API proxy
    - `corsOrigins` (array): Allowed origins for CORS
  - `startup` (object): Startup sequence configuration
    - `waitForBackend` (boolean): Whether frontend should wait for backend
    - `timeout` (number): Timeout for startup sequence in milliseconds
  - `shutdown` (object): Shutdown configuration
    - `gracefulTimeout` (number): Timeout for graceful shutdown in milliseconds

### Process State Object
- **Purpose**: Represents the state of running applications
- **Schema**:
  - `id` (string): Unique identifier for the process
  - `name` (string): Name of the application (frontend/backend)
  - `pid` (number): Process ID
  - `status` (string): Current status (starting, running, stopping, stopped, error)
  - `startTime` (date): When the process was started
  - `endTime` (date): When the process was stopped (if applicable)
  - `healthCheckUrl` (string): URL to check the health of the process
  - `logs` (array): Recent log entries

### Environment Configuration
- **Purpose**: Defines environment-specific settings
- **Schema**:
  - `name` (string): Environment name (dev, staging, prod)
  - `variables` (object): Environment variables mapping
  - `ports` (object): Port assignments
    - `frontend` (number): Frontend port
    - `backend` (number): Backend port
  - `urls` (object): Service URLs
    - `frontend` (string): Frontend URL
    - `backend` (string): Backend URL
    - `apiProxy` (string): API proxy URL

## State Transitions

### Application Startup
- `stopped` → `starting` when startup command is issued
- `starting` → `running` when health check passes
- `starting` → `error` when startup fails or times out
- `error` → `stopped` after error handling

### Application Shutdown
- `running` → `stopping` when shutdown command is issued
- `stopping` → `stopped` when process terminates cleanly
- `stopping` → `error` when process fails to terminate

## Validation Rules

### Orchestration Configuration Validation
- Required: All configuration objects must have required fields
- Port availability: Ports must be available and not in use
- Command validity: Start commands must be executable
- URL format: All URLs must be properly formatted

### Process State Validation
- Unique process IDs: Each process must have a unique identifier
- Valid status: Status must be one of the defined values
- Health check: Health check URLs must be accessible

## Communication Protocols

### Frontend-Backend Communication
- **API Proxy**: Frontend proxies API requests to backend
- **CORS Settings**: Backend allows requests from frontend origin
- **Environment Variables**: Backend URL configured in frontend
- **Health Checks**: Both applications expose health endpoints

### Process Communication
- **Inter-Process Communication**: Via shared environment variables and configuration
- **Signal Handling**: Proper handling of SIGTERM, SIGINT for graceful shutdown
- **Logging**: Centralized logging for troubleshooting