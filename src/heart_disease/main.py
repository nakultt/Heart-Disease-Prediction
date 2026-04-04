from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.heart_disease.core.config import get_settings
from src.heart_disease.core.logging import setup_logging
from src.heart_disease.api.v1.endpoints import prediction
from src.heart_disease.auth.routes import router as auth_router
import logging

# Setup Logging
setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Users live only in RAM: restarting uvicorn clears every account.
    Optionally create a demo user so you can always sign in locally.
    """
    s = get_settings()
    if s.SEED_DEMO_USER:
        from src.heart_disease.auth import password as pwd_utils
        from src.heart_disease.auth import users_store

        if not users_store.username_exists(s.DEMO_USERNAME):
            users_store.add_user(
                s.DEMO_USERNAME,
                pwd_utils.hash_password(s.DEMO_PASSWORD),
            )
            logger.info(
                "Demo account ready: username=%r (disable with SEED_DEMO_USER=false in .env)",
                s.DEMO_USERNAME,
            )
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# CORS config
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(prediction.router, prefix=settings.API_PREFIX, tags=["prediction"])

@app.get("/health")
def health_check():
    return {"status": "ok", "app_name": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.heart_disease.main:app", host="0.0.0.0", port=8000, reload=True)
