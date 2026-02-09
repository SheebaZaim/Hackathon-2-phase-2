# Teachers Planning App - Specification

## Purpose
Convert the current Todo App Phase II into a Professional Teachers Planning Web App with secure multi-user support, proper UI, and fully aligned frontend + backend.

## User Roles
- **Teacher (Only)**: Primary user role with access to planning tools

## Core Entities
- **Teacher**: User account representing an educator
- **Class**: Academic group taught by a teacher
- **Student**: Individual learner within a class
- **Result**: Academic outcome for a student in a subject
- **Subject**: Academic discipline taught in classes

## Features
1. Teacher authentication and profile management
2. Class planning and management
3. Student roster management
4. Academic results tracking
5. Subject-wise record keeping
6. Secure private data per teacher

## Non-Goals
- Student login or direct student access
- Parent portal
- Administrative dashboard for school management
- Gradebook synchronization with external systems

## Technical Requirements
- Secure JWT-based authentication
- Neon PostgreSQL database
- Responsive web interface
- Clean, professional academic UI
- Private data isolation per teacher

## Acceptance Criteria
- Teachers can securely log in and access only their data
- Teachers can create and manage classes
- Teachers can add students to classes
- Teachers can record and view student results by subject
- UI follows professional academic design standards
- All data is properly isolated between teachers