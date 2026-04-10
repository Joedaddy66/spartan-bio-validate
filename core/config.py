import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Railway/Production Defaults
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/bio_vault")
    AGENTVERSE_KEY: str = os.getenv("AGENTVERSE_KEY", "placeholder_key")
    
    # Validation Logic
    MAX_PARALLEL: int = 10
    HT_TARGET_HASH: str = "spartan01_2026_vault"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Gateway & Celery Variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SKYFIRE_API_KEY = os.getenv("SKYFIRE_API_KEY", "")
