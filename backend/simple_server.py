# simple_server.py - The simplest possible FastAPI server
from fastapi import FastAPI
import uvicorn

# Create app
app = FastAPI()

# Single endpoint
@app.get("/")
def hello():
    return {"message": "Mediclinic Backend is working!"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Run server
if __name__ == "__main__":
    print("Starting simple server...")
    print("Open: http://localhost:8000")
    print("Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000)