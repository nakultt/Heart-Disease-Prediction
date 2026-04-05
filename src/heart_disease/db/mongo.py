"""
MongoDB connection (PyMongo). Started on app lifespan, closed on shutdown.
"""

from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConfigurationError, PyMongoError

from src.heart_disease.core.config import get_settings
from src.heart_disease.db.srv_dns import prefer_public_dns_for_srv

_client: MongoClient | None = None


def connect() -> Database:
    """Create client and return the application database."""
    global _client
    settings = get_settings()
    if not settings.MONGODB_URL or not settings.MONGODB_URL.strip():
        raise RuntimeError("MONGODB_URL is not set. Add it to your .env file.")
    url = settings.MONGODB_URL.strip()
    prefer_public_dns_for_srv(url)
    try:
        _client = MongoClient(url, serverSelectionTimeoutMS=10000)
        # Force connection attempt early
        _client.admin.command("ping")
    except ConfigurationError as e:
        hint = ""
        if "mongodb+srv" in url or "srv" in str(e).lower():
            hint = (
                " SRV (mongodb+srv://) needs DNS TXT/SRV lookups. If DNS times out, use a local DB: "
                "set MONGODB_URL=mongodb://127.0.0.1:27017 and run `docker compose up -d`, "
                "or use Atlas's standard (non-SRV) connection string from the cluster dashboard."
            )
        raise RuntimeError(f"Invalid MongoDB configuration: {e}.{hint}") from e
    except PyMongoError as e:
        hint = ""
        if url.startswith("mongodb://127.0.0.1") or url.startswith("mongodb://localhost"):
            hint = (
                " Start MongoDB locally (e.g. `docker compose up -d` from the project root) "
                "or point MONGODB_URL at a reachable server."
            )
        raise RuntimeError(f"Cannot connect to MongoDB: {e}.{hint}") from e
    db = _client[settings.MONGODB_DB_NAME]
    _ensure_indexes(db)
    return db


def disconnect() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_db() -> Database:
    if _client is None:
        raise RuntimeError("MongoDB is not connected. Did the app lifespan run?")
    return _client[get_settings().MONGODB_DB_NAME]


def users_coll() -> Collection[Any]:
    return get_db()["users"]


def predictions_coll() -> Collection[Any]:
    return get_db()["predictions"]


def _ensure_indexes(db: Database) -> None:
    db["users"].create_index("username_lower", unique=True)
    db["predictions"].create_index([("username_lower", ASCENDING), ("created_at", ASCENDING)])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
