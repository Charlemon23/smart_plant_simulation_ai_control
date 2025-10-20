import os
from pydantic import BaseModel


class Settings(BaseModel):
    # === Database ===
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "smartplant")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "smartplant")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "smartplant")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))

    # === Redis ===
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))

    # === Backend runtime ===
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    # === Codespaces dynamic environment ===
    # GitHub Codespaces automatically injects CODESPACE_NAME
    CODESPACE_NAME: str | None = os.getenv("CODESPACE_NAME")
    CODESPACE_DOMAIN: str = "app.github.dev"

    # Construct dynamic backend + CORS origins if inside Codespaces
    @property
    def BACKEND_URL(self) -> str:
        """Return full backend URL based on environment (Codespaces or local)."""
        if self.CODESPACE_NAME:
            return f"https://{self.CODESPACE_NAME}-{self.BACKEND_PORT}.{self.CODESPACE_DOMAIN}"
        return f"http://localhost:{self.BACKEND_PORT}"

    @property
    def CORS_ORIGINS(self) -> list[str]:
        """Allow Codespaces frontend and localhost by default."""
        origins = [
            "http://localhost:8080",
            "http://127.0.0.1:8080",
        ]
        if self.CODESPACE_NAME:
            # Frontend is usually Vite on port 5173
            origins.append(f"https://{self.CODESPACE_NAME}-5173.{self.CODESPACE_DOMAIN}")
        return origins


settings = Settings()
