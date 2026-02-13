"""Script to show database tables and data"""
import os
import sys
import psycopg2
from dotenv import load_dotenv
from tabulate import tabulate

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def show_database():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    print("\n" + "="*80)
    print("NEON DATABASE TABLES AND DATA")
    print("="*80)

    # Show all tables
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()

    print("\nTABLES IN DATABASE:")
    print("-" * 80)
    for table in tables:
        print(f"  - {table[0]}")

    # Show users table
    print("\n" + "="*80)
    print("USERS TABLE")
    print("="*80)
    cursor.execute("""
        SELECT id, email, first_name, last_name, created_at
        FROM users
        ORDER BY created_at DESC
        LIMIT 10;
    """)
    users = cursor.fetchall()
    if users:
        headers = ['ID', 'Email', 'First Name', 'Last Name', 'Created At']
        print(tabulate(users, headers=headers, tablefmt='grid'))
    else:
        print("No users found")

    # Show tasks table
    print("\n" + "="*80)
    print("TASKS TABLE")
    print("="*80)
    cursor.execute("""
        SELECT id, title, completed, priority, due_date, category, created_at
        FROM tasks
        ORDER BY created_at DESC
        LIMIT 10;
    """)
    tasks = cursor.fetchall()
    if tasks:
        headers = ['ID', 'Title', 'Completed', 'Priority', 'Due Date', 'Category', 'Created At']
        print(tabulate(tasks, headers=headers, tablefmt='grid'))
    else:
        print("No tasks found")

    # Show counts
    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80)

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = true")
    completed_count = cursor.fetchone()[0]

    print(f"  • Total Users: {user_count}")
    print(f"  • Total Tasks: {task_count}")
    print(f"  • Completed Tasks: {completed_count}")
    print(f"  • Active Tasks: {task_count - completed_count}")

    print("\n" + "="*80)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    show_database()
