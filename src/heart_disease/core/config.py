from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Heart Disease Prediction API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # ML Settings
    MODEL_DIR: str = "."

    # JWT auth (override JWT_SECRET_KEY in production via .env)
    JWT_SECRET_KEY: str = "dev-only-change-me-use-openssl-rand-hex-32"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours for demos

    # Optional demo account (in-memory resets when the server restarts anyway).
    # Set SEED_DEMO_USER=false in .env for production-like runs.
    SEED_DEMO_USER: bool = True
    DEMO_USERNAME: str = "demo"
    DEMO_PASSWORD: str = "demo123"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
