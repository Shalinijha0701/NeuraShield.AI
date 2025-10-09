import uvicorn
import sys
from pathlib import Path

def main():
    print("Starting NeuraShield.AI API Server...")
    print("Neural Shields: ACTIVE")
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError:
        print("Installing uvicorn...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'uvicorn', 'fastapi'])
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()