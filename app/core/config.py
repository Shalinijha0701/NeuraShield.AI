from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/neurashield"
    REDIS_URL: str = "redis://localhost:6379"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    
    # AI Models
    HUGGINGFACE_TOKEN: Optional[str] = None
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: str = "us-west1-gcp"
    
    # Security
    SECRET_KEY: str = "neurashield-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Neural Shields Configuration
    CODE_BRAIN_MODEL: str = "microsoft/codebert-base"
    SECURITY_SHIELD_THRESHOLD: float = 0.7
    DEVOPS_OPTIMIZER_LEARNING_RATE: float = 0.001
    
    class Config:
        env_file = ".env"

settings = Settings()