-- Migration: Make first_name and last_name nullable with defaults
-- Date: 2026-02-10
-- Purpose: Fix database schema mismatch - allow registration without first_name/last_name

-- Make columns nullable
ALTER TABLE users ALTER COLUMN first_name DROP NOT NULL;
ALTER TABLE users ALTER COLUMN last_name DROP NOT NULL;

-- Set default values
ALTER TABLE users ALTER COLUMN first_name SET DEFAULT '';
ALTER TABLE users ALTER COLUMN last_name SET DEFAULT '';

-- Update any existing NULL values to empty strings (if any)
UPDATE users SET first_name = '' WHERE first_name IS NULL;
UPDATE users SET last_name = '' WHERE last_name IS NULL;
