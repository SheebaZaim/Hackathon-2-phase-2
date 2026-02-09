# Data Model: Teacher Planning App

## Overview
This document outlines the data models for the teacher planning application. The models follow the SQLModel specification and implement the required data isolation between users.

## Core Entities

### User Model
- **Purpose**: Represents a teacher user in the system
- **Fields**:
  - `id` (UUID/int): Unique identifier for the user
  - `email` (str): User's email address (unique)
  - `password_hash` (str): Hashed password for authentication
  - `first_name` (str): User's first name
  - `last_name` (str): User's last name
  - `created_at` (datetime): Timestamp of account creation
  - `updated_at` (datetime): Timestamp of last update
- **Relationships**:
  - One-to-many with SchoolPlanning
  - One-to-many with StudentResult
  - One-to-many with Task

### SchoolPlanning Model
- **Purpose**: Represents a school planning (lesson plan, schedule, etc.) created by a teacher
- **Fields**:
  - `id` (UUID/int): Unique identifier for the planning
  - `title` (str): Title of the planning
  - `description` (str): Detailed description of the planning
  - `subject` (str): Subject area (Math, Science, etc.)
  - `grade_level` (str): Grade level (K-12, etc.)
  - `date` (datetime): Date for the planning
  - `duration` (int): Duration in minutes
  - `materials_needed` (str): Materials required for the planning
  - `learning_objectives` (str): Learning objectives for the planning
  - `class_size` (int): Number of students in the class
  - `teaching_method` (str): Teaching method (lecture, group work, etc.)
  - `assessment_type` (str): Type of assessment (quiz, project, etc.)
  - `standards_addressed` (str): Educational standards addressed
  - `previous_knowledge_required` (str): Previous knowledge required from students
  - `extension_activities` (str): Extension activities for advanced students
  - `differentiation_strategies` (str): Strategies for different learning needs
  - `resources_links` (str): Links to additional resources
  - `user_id` (UUID/int): Foreign key linking to the owning user
  - `created_at` (datetime): Timestamp of creation
  - `updated_at` (datetime): Timestamp of last update
- **Relationships**:
  - Many-to-one with User (owner)

### StudentResult Model
- **Purpose**: Represents student results/grades uploaded by a teacher
- **Fields**:
  - `id` (UUID/int): Unique identifier for the result
  - `student_name` (str): Name of the student
  - `assignment_title` (str): Title of the assignment/test
  - `score` (float): Numeric score
  - `max_score` (float): Maximum possible score
  - `percentage` (float): Calculated percentage
  - `grade_letter` (str): Letter grade (A, B, C, etc.)
  - `subject` (str): Subject area
  - `date_recorded` (datetime): Date the result was recorded
  - `comments` (str): Teacher's comments
  - `user_id` (UUID/int): Foreign key linking to the owning user
  - `created_at` (datetime): Timestamp of creation
  - `updated_at` (datetime): Timestamp of last update
- **Relationships**:
  - Many-to-one with User (owner)

### Task Model
- **Purpose**: Represents a task/to-do item for a teacher
- **Fields**:
  - `id` (UUID/int): Unique identifier for the task
  - `title` (str): Title of the task
  - `description` (str): Detailed description of the task
  - `due_date` (datetime): Due date for the task
  - `category` (str): Category of the task (lesson planning, grading, meeting, parent conference, etc.)
  - `priority` (str): Priority level (low, medium, high)
  - `completed` (bool): Whether the task is completed
  - `completed_at` (datetime): When the task was completed (if applicable)
  - `assigned_class` (str): Class to which the task applies (if applicable)
  - `subject_area` (str): Subject area related to the task
  - `estimated_time` (int): Estimated time to complete in minutes
  - `actual_time` (int): Actual time taken to complete in minutes
  - `related_planning_id` (UUID/int): Reference to related school planning (foreign key)
  - `students_involved` (str): Students involved in the task (comma-separated list)
  - `recurring` (bool): Whether the task is recurring
  - `recurring_frequency` (str): Frequency of recurrence (daily, weekly, monthly)
  - `reminders_enabled` (bool): Whether to send reminders for this task
  - `remind_before` (int): Minutes before due date to send reminder
  - `user_id` (UUID/int): Foreign key linking to the owning user
  - `created_at` (datetime): Timestamp of creation
  - `updated_at` (datetime): Timestamp of last update
- **Relationships**:
  - Many-to-one with User (owner)
  - Many-to-one with SchoolPlanning (optional, related planning)

## State Transitions

### Task State Transitions
- `incomplete` → `completed` when task is marked as complete
- `completed` → `incomplete` when task completion is reversed

### StudentResult State Transitions
- `draft` → `finalized` when result is finalized
- `finalized` → `updated` when score is modified after finalization

## Validation Rules

### User Validation
- Email must be in valid format
- Password must meet security requirements (min length, complexity)
- Email must be unique across all users

### SchoolPlanning Validation
- Title is required and must be between 3-100 characters
- Date must be in the future or present
- Subject must be selected from predefined list
- Grade level must be valid (K-12)

### StudentResult Validation
- Score must be numeric and between 0 and max_score
- Max_score must be positive
- Student name is required
- Assignment title is required
- Date must be in the past or present

### Task Validation
- Title is required and must be between 3-100 characters
- Due date must be in the future
- Category must be from predefined list
- Priority must be low, medium, or high

## Relationships

### User to SchoolPlanning
- One-to-many relationship
- User "owns" multiple school plannings
- When user is deleted, their plannings are also deleted (cascade)

### User to StudentResult
- One-to-many relationship
- User "owns" multiple student results
- When user is deleted, their results are also deleted (cascade)

### User to Task
- One-to-many relationship
- User "owns" multiple tasks
- When user is deleted, their tasks are also deleted (cascade)

## Indexes

### User Model
- Index on email field for fast lookup during authentication

### SchoolPlanning Model
- Index on user_id for fast retrieval of user's plannings
- Index on date for chronological sorting
- Composite index on user_id and date for efficient filtering

### StudentResult Model
- Index on user_id for fast retrieval of user's results
- Index on student_name for searching
- Index on date_recorded for chronological sorting
- Composite index on user_id and subject for efficient filtering

### Task Model
- Index on user_id for fast retrieval of user's tasks
- Index on due_date for sorting by deadline
- Index on completed for filtering completed/incomplete tasks
- Composite index on user_id and completed status for efficient filtering