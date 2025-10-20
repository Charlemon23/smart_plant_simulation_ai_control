import os
from pydantic import BaseModel

class Settings(BaseModel):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER","smartplant")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD","smartplant")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB","smartplant")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST","db")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT","5432"))
    REDIS_HOST: str = os.getenv("REDIS_HOST","redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT","6379"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS","http://localhost:8080")

settings = Settings()
