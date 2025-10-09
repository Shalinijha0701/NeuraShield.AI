from fastapi import FastAPI
import uvicorn

app = FastAPI(title="NeuraShield.AI", description="Self-Learning AI Guardian")

@app.get("/")
def root():
    return {"message": "NeuraShield.AI Active", "status": "running", "shields": "online"}

@app.get("/health")
def health():
    return {"status": "healthy", "neural_shields": "active"}

@app.post("/analyze")
def analyze(code: str):
    # Simple analysis simulation
    issues = code.count("eval") + code.count("password")
    trust_score = max(0, 1 - (issues / 10))
    return {
        "trust_score": trust_score,
        "issues_found": issues,
        "status": "analyzed",
        "recommendation": "Deploy" if trust_score > 0.7 else "Review needed"
    }

if __name__ == "__main__":
    print("NeuraShield.AI - Self-Learning AI Guardian")
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)