# API Contract: Verification Service

**Feature**: 002-verify-and-update-setup
**Date**: 2026-02-07
**Version**: 1.0

## Overview

This document defines the API contract for the verification service that checks system components and reports on missing or incomplete elements.

## Base URL

`http://localhost:3001/api/v1`

## Endpoints

### GET /verification/status

Retrieves the current verification status of system components.

#### Request

No request body required.

#### Response

**Success (200 OK)**

```json
{
  "status": "complete|in-progress|error",
  "lastRun": "ISO date string",
  "reportId": "uuid",
  "summary": {
    "totalComponents": 15,
    "checkedComponents": 12,
    "passedComponents": 8,
    "failedComponents": 3,
    "missingComponents": 1,
    "complianceScore": 85.7
  }
}
```

### GET /verification/report/{reportId}

Retrieves a detailed verification report.

#### Path Parameters

- `reportId`: The ID of the report to retrieve

#### Response

**Success (200 OK)**

```json
{
  "id": "uuid",
  "timestamp": "ISO date string",
  "version": "string",
  "componentsChecked": [
    {
      "name": "Authentication Service",
      "status": "pass",
      "details": "Service is running and responding to requests",
      "compliant": true,
      "errors": [],
      "warnings": []
    },
    {
      "name": "Database Connection",
      "status": "fail",
      "details": "Connection failed due to incorrect credentials",
      "compliant": false,
      "errors": ["Connection refused"],
      "warnings": []
    },
    {
      "name": "Logging System",
      "status": "missing",
      "details": "No logging system detected",
      "compliant": false,
      "errors": ["Component not found"],
      "warnings": []
    }
  ],
  "totalComponents": 15,
  "passedComponents": 8,
  "failedComponents": 3,
  "missingComponents": 1,
  "complianceScore": 85.7,
  "overallStatus": "partial"
}
```

### POST /verification/run

Initiates a new verification run.

#### Request

No request body required.

#### Response

**Success (202 Accepted)**

```json
{
  "message": "Verification process started",
  "jobId": "uuid",
  "estimatedDuration": "seconds number"
}
```

### GET /verification/job/{jobId}

Checks the status of a verification job.

#### Path Parameters

- `jobId`: The ID of the verification job

#### Response

**Success (200 OK)**

```json
{
  "id": "uuid",
  "status": "queued|running|completed|failed",
  "progress": {
    "currentStep": "string",
    "completedSteps": "number",
    "totalSteps": "number",
    "percentage": "number"
  },
  "createdAt": "ISO date string",
  "updatedAt": "ISO date string"
}
```

## Error Responses

All error responses follow this structure:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "string (optional)"
  }
}
```

Common error codes:
- `VERIFICATION_NOT_FOUND`: The specified verification report or job doesn't exist
- `VERIFICATION_FAILED`: The verification process failed unexpectedly
- `UNAUTHORIZED`: Access denied due to missing or invalid credentials
- `INTERNAL_ERROR`: An unexpected error occurred on the server

## Authentication

Some endpoints may require authentication using JWT tokens passed in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

## Rate Limiting

This API implements rate limiting to prevent abuse:
- 100 requests per minute per IP address
- 10 requests per minute for authenticated users