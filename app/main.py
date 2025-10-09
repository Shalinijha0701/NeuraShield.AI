from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(
    title="NeuraShield.AI",
    description="Self-Learning AI Guardian for Modern DevOps",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {
        "message": "NeuraShield.AI - Self-Learning AI Guardian",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "neural_shields": "active"}