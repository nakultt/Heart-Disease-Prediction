"""
Simple in-memory user storage for learning projects.

Keys are usernames (lowercase). Values hold the hashed password only—never store plain text.
"""

from typing import TypedDict


class UserRecord(TypedDict):
    """One row in our fake 'database'."""

    username: str
    hashed_password: str


# Global dict: username -> user record (survives until the server restarts).
users_db: dict[str, UserRecord] = {}


def username_exists(username: str) -> bool:
    """Return True if this username is already registered."""
    return username.lower() in users_db


def add_user(username: str, hashed_password: str) -> None:
    """Save a new user. Caller must hash the password first."""
    key = username.lower()
    users_db[key] = UserRecord(username=username, hashed_password=hashed_password)


def get_user(username: str) -> UserRecord | None:
    """Fetch a user by username, or None if not found."""
    return users_db.get(username.lower())
