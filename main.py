import uvicorn
from app import app  # Import the FastAPI app instance

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
