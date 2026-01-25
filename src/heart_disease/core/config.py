from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Heart Disease Prediction API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # ML Settings
    MODEL_DIR: str = "."
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
