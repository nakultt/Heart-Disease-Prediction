"""Convenience backend entrypoint for local development."""

import uvicorn

from src.heart_disease.main import app


if __name__ == "__main__":
    uvicorn.run("src.heart_disease.main:app", host="0.0.0.0", port=8000, reload=True)
