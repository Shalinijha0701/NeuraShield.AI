from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from neo4j import GraphDatabase
import redis
from app.core.config import settings

# PostgreSQL
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Neo4j
neo4j_driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

# Redis
redis_client = redis.from_url(settings.REDIS_URL)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_neo4j_session():
    return neo4j_driver.session()

async def init_db():
    """Initialize database connections and create tables"""
    Base.metadata.create_all(bind=engine)
    
    # Test connections
    try:
        redis_client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
    
    try:
        with neo4j_driver.session() as session:
            session.run("RETURN 1")
        print("✅ Neo4j connection successful")
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")