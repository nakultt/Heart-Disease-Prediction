"""
Gradient Boosting predictor — drop-in replacement for the PyTorch HeartDiseasePredictor.

Exposes the same `.predict(dict) -> float` interface used by the API layer so
`predict.py:get_predictor()` can return either backend transparently.
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Dict


class GBHeartDiseasePredictor:
    """Wraps a fitted GradientBoostingClassifier + ColumnTransformer."""

    def __init__(self, model_path: str, preprocessor_path: str):
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)

    def predict(self, input_data: Dict[str, Any]) -> float:
        """Return P(heart_disease) ∈ [0, 1]."""
        df = pd.DataFrame([input_data])

        X_processed = self.preprocessor.transform(df)
        if hasattr(X_processed, "toarray"):
            X_processed = X_processed.toarray()

        prob = self.model.predict_proba(X_processed)[0, 1]
        return float(prob)
