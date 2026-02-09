import uvicorn
from minimal_backend import app

if __name__ == "__main__":
    print("Starting backend server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)