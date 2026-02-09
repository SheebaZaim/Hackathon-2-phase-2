import uvicorn
import sys
import os

# Add the src directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import app

if __name__ == "__main__":
    print("Starting the Todo App Backend Server...")
    print("Visit http://127.0.0.1:8000 to access the API")
    print("Press Ctrl+C to stop the server")

    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )