"""User documents in MongoDB (no password in API responses)."""

from __future__ import annotations

from typing import Any

from pymongo import ReturnDocument
from pymongo.collection import Collection

from src.heart_disease.db.mongo import users_coll, utc_now


def gender_to_sex(gender: str) -> int:
    """Map profile gender to model sex: 1 = male, 0 = female/other."""
    g = (gender or "").lower().strip()
    if g == "male":
        return 1
    return 0


def find_user_by_username(username: str) -> dict[str, Any] | None:
    key = username.strip().lower()
    return users_coll().find_one({"username_lower": key})


def username_taken(username: str) -> bool:
    return find_user_by_username(username) is not None


def insert_user(
    username: str,
    password_hash: str,
    age: int,
    gender: str,
    weight_kg: float,
    height_cm: float,
    smoking: str = "never",
    stress: str = "low",
) -> None:
    now = utc_now()
    doc: dict[str, Any] = {
        "username": username.strip(),
        "username_lower": username.strip().lower(),
        "password_hash": password_hash,
        "age": age,
        "gender": gender.strip().lower(),
        "weight_kg": weight_kg,
        "height_cm": height_cm,
        "smoking": smoking,
        "stress": stress,
        "created_at": now,
        "updated_at": now,
    }
    users_coll().insert_one(doc)


def profile_public(doc: dict[str, Any]) -> dict[str, Any]:
    """Strip sensitive fields; coerce BSON/extended types so Pydantic JSON works."""
    return {
        "username": str(doc["username"]),
        "age": int(doc["age"]),
        "gender": str(doc["gender"]),
        "weight_kg": float(doc["weight_kg"]),
        "height_cm": float(doc["height_cm"]),
        "smoking": str(doc["smoking"]),
        "stress": str(doc["stress"]),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


def update_user_profile(username: str, updates: dict[str, Any]) -> dict[str, Any] | None:
    """Apply allowed field updates. Returns updated public profile or None."""
    key = username.strip().lower()
    allowed = {
        "age",
        "gender",
        "weight_kg",
        "height_cm",
        "smoking",
        "stress",
    }
    patch = {k: v for k, v in updates.items() if k in allowed and v is not None}
    if not patch:
        u = find_user_by_username(username)
        return profile_public(u) if u else None
    patch["updated_at"] = utc_now()
    if "gender" in patch and isinstance(patch["gender"], str):
        patch["gender"] = patch["gender"].strip().lower()
    coll: Collection[Any] = users_coll()
    res = coll.find_one_and_update(
        {"username_lower": key},
        {"$set": patch},
        return_document=ReturnDocument.AFTER,
    )
    return profile_public(res) if res else None

