# Database Migrations

## Current Issue

The `users` table has `first_name` and `last_name` columns with NOT NULL constraints, but the registration endpoint doesn't collect these fields. This causes registration to fail with:

```
null value in column 'first_name' of relation 'users' violates not-null constraint
```

## Solution

Run the migration script to make these fields nullable with default empty strings.

## How to Run Migration

### Option 1: Using Python Script (Recommended)

```bash
cd backend/migrations
python run_migration.py 001_fix_users_table_nullable_fields.sql
```

This will:
- Connect to your Neon database using DATABASE_URL from .env
- Execute the SQL migration
- Show success or error message

### Option 2: Manual SQL Execution

Connect to your Neon database via psql or Neon's web console and run:

```sql
-- Make columns nullable
ALTER TABLE users ALTER COLUMN first_name DROP NOT NULL;
ALTER TABLE users ALTER COLUMN last_name DROP NOT NULL;

-- Set default values
ALTER TABLE users ALTER COLUMN first_name SET DEFAULT '';
ALTER TABLE users ALTER COLUMN last_name SET DEFAULT '';

-- Update any existing NULL values to empty strings (if any)
UPDATE users SET first_name = '' WHERE first_name IS NULL;
UPDATE users SET last_name = '' WHERE last_name IS NULL;
```

### Option 3: Using Neon's Web Console

1. Go to https://console.neon.tech
2. Select your project and database
3. Open the SQL Editor
4. Copy and paste the SQL from `001_fix_users_table_nullable_fields.sql`
5. Click "Run"

## After Migration

Once the migration is complete:

1. **Test Registration**:
   ```bash
   curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123"}'
   ```

   Should return:
   ```json
   {
     "access_token": "eyJ...",
     "token_type": "bearer"
   }
   ```

2. **Test in Browser**:
   - Go to http://localhost:3000
   - Click "Get Started"
   - Enter email and password
   - Should redirect to dashboard!

## Troubleshooting

### If migration fails with "relation 'users' does not exist"

The users table hasn't been created yet. Run the table creation first:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) DEFAULT '',
    last_name VARCHAR(100) DEFAULT '',
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### If migration fails with "permission denied"

Ensure your DATABASE_URL has proper permissions to ALTER tables.

### If you see "psycopg2 not found"

Install it:
```bash
pip install psycopg2-binary
```

## Migration History

- `001_fix_users_table_nullable_fields.sql` - Make first_name and last_name nullable with defaults
