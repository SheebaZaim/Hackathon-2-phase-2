"""
Migration runner script - Execute SQL migrations against Neon database
Usage: python run_migration.py 001_fix_users_table_nullable_fields.sql
"""
import sys
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in environment variables")
    print("Please ensure .env file exists with DATABASE_URL")
    sys.exit(1)


def run_migration(sql_file: str):
    """Execute a SQL migration file against the database"""

    # Read SQL file
    sql_path = Path(__file__).parent / sql_file

    if not sql_path.exists():
        print(f"ERROR: Migration file not found: {sql_path}")
        sys.exit(1)

    with open(sql_path, 'r') as f:
        sql_content = f.read()

    print(f"Running migration: {sql_file}")
    print("=" * 60)
    print(sql_content)
    print("=" * 60)

    # Connect and execute
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Execute the SQL
        cursor.execute(sql_content)
        conn.commit()

        print("[SUCCESS] Migration completed successfully!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("[ERROR] Migration failed with error:")
        print(f"   {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_migration.py <migration_file.sql>")
        print("Example: python run_migration.py 001_fix_users_table_nullable_fields.sql")
        sys.exit(1)

    migration_file = sys.argv[1]
    run_migration(migration_file)
