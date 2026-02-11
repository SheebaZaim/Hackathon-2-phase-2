-- Migration: Make tasks table compatible with simple Todo App model
-- Date: 2026-02-11
-- Purpose: Fix database schema mismatch - make extra columns nullable

-- Make columns nullable that aren't in the Task model
ALTER TABLE tasks ALTER COLUMN due_date DROP NOT NULL;
ALTER TABLE tasks ALTER COLUMN category DROP NOT NULL;
ALTER TABLE tasks ALTER COLUMN priority DROP NOT NULL;
ALTER TABLE tasks ALTER COLUMN assigned_class DROP NOT NULL;
ALTER TABLE tasks ALTER COLUMN subject_area DROP NOT NULL;
ALTER TABLE tasks ALTER COLUMN recurring_frequency DROP NOT NULL;

-- Set default values
ALTER TABLE tasks ALTER COLUMN due_date SET DEFAULT NULL;
ALTER TABLE tasks ALTER COLUMN category SET DEFAULT '';
ALTER TABLE tasks ALTER COLUMN priority SET DEFAULT 'medium';
ALTER TABLE tasks ALTER COLUMN completed SET DEFAULT false;
ALTER TABLE tasks ALTER COLUMN recurring SET DEFAULT false;
ALTER TABLE tasks ALTER COLUMN reminders_enabled SET DEFAULT false;

-- Update any existing NULL values to defaults (if any)
UPDATE tasks SET category = '' WHERE category IS NULL;
UPDATE tasks SET priority = 'medium' WHERE priority IS NULL;
UPDATE tasks SET completed = false WHERE completed IS NULL;
UPDATE tasks SET recurring = false WHERE recurring IS NULL;
UPDATE tasks SET reminders_enabled = false WHERE reminders_enabled IS NULL;
