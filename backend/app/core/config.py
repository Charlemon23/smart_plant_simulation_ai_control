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

    # === Codespaces Environment ===
    CODESPACE_NAME: str | None = os.getenv("CODESPACE_NAME")
    CODESPACE_DOMAIN: str = "app.github.dev"

    @property
    def BACKEND_URL(self) -> str:
        """Build the full backend URL automatically for Codespaces or local use."""
        if self.CODESPACE_NAME:
            return f"https://{self.CODESPACE_NAME}-{self.BACKEND_PORT}.{self.CODESPACE_DOMAIN}"
        return f"http://localhost:{self.BACKEND_PORT}"

    @property
    def CORS_ORIGINS(self) -> list[str]:
        """
        Allow localhost and ANY Codespaces frontend URL.
        This uses a wildcard pattern that matches all subdomains of this Codespace.
        """
        origins = [
            "http://localhost",
            "http://localhost:8080",
            "http://127.0.0.1",
            "http://127.0.0.1:8080",
        ]

        if self.CODESPACE_NAME:
            # Allow any frontend port or path within this Codespace domain
            # Example: https://super-train-wrrwrx6r4gw535pqj-ANYPORT.app.github.dev
            base_pattern = f"https://{self.CODESPACE_NAME}-*.{self.CODESPACE_DOMAIN}"
            origins.append(base_pattern)

            # Also allow the root codespace domain for other API clients
            origins.append(f"https://{self.CODESPACE_NAME}.{self.CODESPACE_DOMAIN}")

        # Optional: allow internal API calls from the backend itself
        origins.append(self.BACKEND_URL)

        return origins


settings = Settings()
