-- Migration: Add todo_lists table and update tasks table
-- Date: 2026-02-12
-- Purpose: Add todo lists feature to organize tasks into different lists

-- Create todo_lists table
CREATE TABLE IF NOT EXISTS todo_lists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    color VARCHAR(20) DEFAULT '#3B82F6',
    icon VARCHAR(10) DEFAULT '📝',
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_todo_lists_user_id ON todo_lists(user_id);

-- Add todo_list_id column to tasks table (nullable for now)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS todo_list_id UUID REFERENCES todo_lists(id) ON DELETE SET NULL;

-- Create index on todo_list_id for faster queries
CREATE INDEX IF NOT EXISTS idx_tasks_todo_list_id ON tasks(todo_list_id);

-- Create a default "My Tasks" list for each existing user
INSERT INTO todo_lists (user_id, name, description, color, icon, is_default)
SELECT
    id as user_id,
    'My Tasks' as name,
    'Default task list' as description,
    '#3B82F6' as color,
    '📝' as icon,
    TRUE as is_default
FROM users
ON CONFLICT DO NOTHING;

-- Update existing tasks to belong to the default list of their user
UPDATE tasks t
SET todo_list_id = (
    SELECT tl.id
    FROM todo_lists tl
    WHERE tl.user_id = t.user_id
    AND tl.is_default = TRUE
    LIMIT 1
)
WHERE t.todo_list_id IS NULL;
