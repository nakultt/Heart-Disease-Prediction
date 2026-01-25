from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.heart_disease.core.config import get_settings
from src.heart_disease.core.logging import setup_logging
from src.heart_disease.api.v1.endpoints import prediction
import logging

# Setup Logging
setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# CORS config
origins = [
    "http://localhost:5173", # Vite default
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(prediction.router, prefix=settings.API_PREFIX, tags=["prediction"])

@app.get("/health")
def health_check():
    return {"status": "ok", "app_name": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.heart_disease.main:app", host="0.0.0.0", port=8000, reload=True)
