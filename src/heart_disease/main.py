from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.heart_disease.core.config import get_settings
from src.heart_disease.core.logging import setup_logging
from src.heart_disease.api.v1.endpoints import history, prediction, profile
from src.heart_disease.auth.routes import router as auth_router
import logging

setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()
logger.info("Active ML Model Type: %s", settings.MODEL_TYPE.upper())


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Connect MongoDB on startup; disconnect on shutdown. Optionally seed demo user."""
    from pymongo.errors import DuplicateKeyError

    from src.heart_disease.auth import password as pwd_utils
    from src.heart_disease.db import mongo, users_repo

    mongo.connect()
    try:
        s = get_settings()
        if s.SEED_DEMO_USER and not users_repo.username_taken(s.DEMO_USERNAME):
            try:
                users_repo.insert_user(
                    username=s.DEMO_USERNAME,
                    password_hash=pwd_utils.hash_password(s.DEMO_PASSWORD),
                    age=40,
                    gender="male",
                    weight_kg=75.0,
                    height_cm=175.0,
                    smoking="never",
                    stress="low",
                )
                logger.info(
                    "Demo account created in MongoDB: %r (set SEED_DEMO_USER=false to disable)",
                    s.DEMO_USERNAME,
                )
            except DuplicateKeyError:
                logger.warning("Demo user already exists (duplicate key); continuing.")
        yield
    finally:
        mongo.disconnect()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# Any localhost / 127.0.0.1 port (Vite may use 5173, 5174, …). Also allow direct LAN IP for dev.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$|https?://192\.168\.\d+\.\d+(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(prediction.router, prefix=settings.API_PREFIX, tags=["prediction"])
app.include_router(profile.router, prefix=settings.API_PREFIX, tags=["profile"])
app.include_router(history.router, prefix=settings.API_PREFIX, tags=["history"])


@app.get("/health")
def health_check():
    return {"status": "ok", "app_name": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn

    # 0.0.0.0 accepts connections via 127.0.0.1 and localhost (works with Vite proxy).
    uvicorn.run("src.heart_disease.main:app", host="0.0.0.0", port=8000, reload=True)
