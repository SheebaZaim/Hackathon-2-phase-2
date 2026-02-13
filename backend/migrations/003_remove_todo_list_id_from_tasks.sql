-- Migration: Remove todo_list_id column from tasks table
-- Date: 2026-02-13
-- Purpose: Simplify Task model - remove unused todo_list_id foreign key

-- Drop the foreign key constraint first
ALTER TABLE tasks DROP CONSTRAINT IF EXISTS tasks_todo_list_id_fkey;

-- Drop the column
ALTER TABLE tasks DROP COLUMN IF EXISTS todo_list_id;
