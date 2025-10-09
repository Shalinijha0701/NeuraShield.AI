from app.main import app
import uvicorn

if __name__ == "__main__":
    print("NeuraShield.AI Starting...")
    print("API: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)