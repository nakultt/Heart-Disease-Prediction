"""
Password hashing with bcrypt.

We use the `bcrypt` package directly. passlib's bcrypt handler often breaks with
bcrypt 4.1+ (version detection / 72-byte checks), so this avoids that stack.
"""

import bcrypt


def hash_password(plain_password: str) -> str:
    """Hash a password for storage (bcrypt + random salt)."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if the password matches the stored bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )
