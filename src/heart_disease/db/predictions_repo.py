"""Prediction history documents."""

from __future__ import annotations

from typing import Any

from src.heart_disease.db.mongo import predictions_coll, utc_now


def insert_history(
    username: str,
    clinical_input: dict[str, Any],
    full_model_input: dict[str, Any],
    prediction: int,
    probability: float,
    risk_level: str,
) -> str:
    """Save one prediction run; returns inserted id as string."""
    u = username.strip()
    doc: dict[str, Any] = {
        "username": u,
        "username_lower": u.lower(),
        "clinical_input": clinical_input,
        "full_model_input": full_model_input,
        "prediction": prediction,
        "probability": probability,
        "risk_level": risk_level,
        "created_at": utc_now(),
    }
    res = predictions_coll().insert_one(doc)
    return str(res.inserted_id)


def list_for_user(username: str, limit: int = 100) -> list[dict[str, Any]]:
    """Newest first."""
    key = username.strip().lower()
    cur = (
        predictions_coll()
        .find({"username_lower": key})
        .sort("created_at", -1)
        .limit(limit)
    )
    out: list[dict[str, Any]] = []
    for doc in cur:
        oid = doc.pop("_id", None)
        clin = doc.get("clinical_input")
        if isinstance(clin, dict):
            clin = {k: float(v) if isinstance(v, (int, float)) else v for k, v in clin.items()}
        out.append(
            {
                "id": str(oid) if oid else "",
                "created_at": doc.get("created_at"),
                "prediction": int(doc.get("prediction", 0)),
                "probability": float(doc.get("probability", 0.0)),
                "risk_level": str(doc.get("risk_level", "")),
                "clinical_input": clin,
            }
        )
    return out
