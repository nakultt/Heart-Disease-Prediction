from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def project_root() -> Path:
    """Repo root (contains `src/`, `best_model.pth`, `.env`)."""
    return Path(__file__).resolve().parents[3]


def resolve_model_dir() -> Path:
    """
    Resolve MODEL_DIR against the repo root so ML files load even when uvicorn's cwd is `frontend/` or elsewhere.
    """
    p = Path(get_settings().MODEL_DIR)
    if p.is_absolute():
        return p.resolve()
    return (project_root() / p).resolve()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(project_root() / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Heart Disease Prediction API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    # ML Settings (relative paths are resolved from repo root via `resolve_model_dir`)
    MODEL_DIR: str = "."

    # MongoDB — default local (no SRV/DNS). Override in .env for Atlas; prefer standard mongodb:// URI if SRV DNS fails.
    MONGODB_URL: str = "mongodb://127.0.0.1:27017"
    MONGODB_DB_NAME: str = "heart"

    # JWT auth (override JWT_SECRET_KEY in production via .env)
    JWT_SECRET_KEY: str = "dev-only-change-me-use-openssl-rand-hex-32"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours for demos

    # Optional demo account (in-memory resets when the server restarts anyway).
    # Set SEED_DEMO_USER=false in .env for production-like runs.
    SEED_DEMO_USER: bool = True
    DEMO_USERNAME: str = "demo"
    DEMO_PASSWORD: str = "demo123"

@lru_cache()
def get_settings():
    return Settings()
