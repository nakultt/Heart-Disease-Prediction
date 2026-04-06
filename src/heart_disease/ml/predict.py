"""
Unified predictor factory.

Reads ``MODEL_TYPE`` from the environment (via ``Settings``) and returns
the appropriate predictor backend:

* ``"pytorch"``           → PyTorch MLP  (``best_model.pth`` + ``preprocessor.joblib``)
* ``"gradient_boosting"`` → sklearn GB   (``gb_model.joblib``  + ``gb_preprocessor.joblib``)

Both backends expose the same ``predict(dict) -> float`` interface so the
API layer is completely agnostic.
"""

import logging
from typing import Union

import torch
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any

from src.heart_disease.core.config import get_settings, resolve_model_dir
from src.heart_disease.ml.model import HeartDiseaseClassifier
from src.heart_disease.ml.gb_predict import GBHeartDiseasePredictor

logger = logging.getLogger(__name__)


# ── PyTorch predictor (unchanged logic, just wrapped in the class) ───────────

class HeartDiseasePredictor:
    """PyTorch MLP predictor."""

    def __init__(self, model_path: str, preprocessor_path: str, device: str = "cpu"):
        self.device = torch.device(device)
        self.preprocessor = joblib.load(preprocessor_path)

    def load_model(self, model_path: str, input_dim: int, hidden_dim: int = 64):
        self.model = HeartDiseaseClassifier(input_dim=input_dim, hidden_dim=hidden_dim).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def predict(self, input_data: Dict[str, Any]) -> float:
        df = pd.DataFrame([input_data])

        X_processed = self.preprocessor.transform(df)
        if hasattr(X_processed, "toarray"):
            X_processed = X_processed.toarray()

        X_tensor = torch.tensor(X_processed, dtype=torch.float32).to(self.device)

        if not hasattr(self, "model"):
            raise RuntimeError("Model not loaded — call load_model() first")

        with torch.no_grad():
            logits = self.model(X_tensor)
            prob = torch.sigmoid(logits).item()

        return prob


# ── Factory ──────────────────────────────────────────────────────────────────

def _load_pytorch_predictor() -> HeartDiseasePredictor:
    """Load the PyTorch MLP backend."""
    base = resolve_model_dir()
    preprocessor_path = base / "preprocessor.joblib"
    model_path = base / "best_model.pth"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    predictor = HeartDiseasePredictor(str(model_path), str(preprocessor_path), device=device)

    # Infer input_dim from saved state-dict
    state_dict = torch.load(model_path, map_location="cpu")
    input_dim = state_dict["layer_1.0.weight"].shape[1]

    predictor.load_model(str(model_path), input_dim)
    logger.info("Loaded PyTorch MLP predictor (input_dim=%d, device=%s)", input_dim, device)
    return predictor


def _load_gb_predictor() -> GBHeartDiseasePredictor:
    """Load the Gradient Boosting backend."""
    base = resolve_model_dir()
    model_path = base / "gb_model.joblib"
    preprocessor_path = base / "gb_preprocessor.joblib"

    predictor = GBHeartDiseasePredictor(str(model_path), str(preprocessor_path))
    logger.info("Loaded Gradient Boosting predictor")
    return predictor


def get_predictor() -> Union[HeartDiseasePredictor, GBHeartDiseasePredictor]:
    """
    Return the predictor selected by ``MODEL_TYPE`` in the environment.

    Supported values:
        - ``"pytorch"``           (default) — PyTorch MLP
        - ``"gradient_boosting"`` — sklearn GradientBoostingClassifier
    """
    model_type = get_settings().MODEL_TYPE.lower().strip()

    if model_type == "gradient_boosting":
        return _load_gb_predictor()
    elif model_type == "pytorch":
        return _load_pytorch_predictor()
    else:
        raise ValueError(
            f"Unknown MODEL_TYPE={model_type!r}. "
            f"Expected 'pytorch' or 'gradient_boosting'."
        )
