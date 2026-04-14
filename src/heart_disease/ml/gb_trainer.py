"""
Gradient Boosting trainer for Heart Disease Prediction.

Usage:
    python -m src.heart_disease.ml.gb_trainer --data_path data/heart.csv

Produces:
    gb_model.joblib         — fitted GradientBoostingClassifier
    gb_preprocessor.joblib  — fitted ColumnTransformer (same pipeline as PyTorch)
"""

import argparse
import logging
from pathlib import Path

import joblib
import mlflow
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.heart_disease.ml.dataset import load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train(
    data_path: str,
    n_estimators: int = 300,
    max_depth: int = 3,
    learning_rate: float = 0.05,
    subsample: float = 0.8,
    min_samples_split: int = 5,
    min_samples_leaf: int = 3,
    imbalance_strategy: str = "sample_weight",
    experiment_name: str = "Heart Disease Prediction — Gradient Boosting",
):
    mlflow.set_experiment(experiment_name)

    logger.info("Loading data from %s …", data_path)
    train_dataset, val_dataset, preprocessor = load_data(data_path)

    # Extract raw numpy arrays from the ProcessedHeartDataset wrappers
    X_train = train_dataset.X.numpy()
    y_train = train_dataset.y.numpy().ravel()
    X_val = val_dataset.X.numpy()
    y_val = val_dataset.y.numpy().ravel()

    logger.info(
        "Train samples: %d | Val samples: %d | Features: %d",
        X_train.shape[0],
        X_val.shape[0],
        X_train.shape[1],
    )
    logger.info("Train class distribution: %s", np.bincount(y_train.astype(int)).tolist())
    logger.info("Val class distribution: %s", np.bincount(y_val.astype(int)).tolist())

    with mlflow.start_run():
        params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "subsample": subsample,
            "min_samples_split": min_samples_split,
            "min_samples_leaf": min_samples_leaf,
            "imbalance_strategy": imbalance_strategy,
        }
        mlflow.log_params(params)

        # ── Fit ──────────────────────────────────────────────────────────
        gb = GradientBoostingClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            subsample=subsample,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
        )

        logger.info("Training Gradient Boosting model …")
        X_fit = X_train
        y_fit = y_train
        sample_weight = None
        if imbalance_strategy == "sample_weight":
            sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
            logger.info("Applying class-balanced sample weights during fit.")
        elif imbalance_strategy == "smote":
            try:
                from imblearn.over_sampling import SMOTE
            except ImportError as e:
                raise RuntimeError(
                    "SMOTE requested but imbalanced-learn is not installed. "
                    "Run: pip install imbalanced-learn"
                ) from e
            sm = SMOTE(random_state=42)
            X_fit, y_fit = sm.fit_resample(X_train, y_train)
            logger.info("Applied SMOTE. Resampled distribution: %s", np.bincount(y_fit.astype(int)).tolist())
        elif imbalance_strategy != "none":
            raise ValueError("imbalance_strategy must be one of: sample_weight, smote, none")

        gb.fit(X_fit, y_fit, sample_weight=sample_weight)

        # Calibrate the model for smoother probabilities
        logger.info("Calibrating the model probabilities …")
        calibrated_gb = CalibratedClassifierCV(estimator=gb, method="sigmoid", cv="prefit")
        calibrated_gb.fit(X_val, y_val)

        # ── Evaluate ─────────────────────────────────────────────────────
        y_pred_train = calibrated_gb.predict(X_train)
        y_pred_val = calibrated_gb.predict(X_val)
        y_prob_val = calibrated_gb.predict_proba(X_val)[:, 1]

        train_acc = accuracy_score(y_train, y_pred_train)
        val_acc = accuracy_score(y_val, y_pred_val)
        val_precision = precision_score(y_val, y_pred_val, zero_division=0)
        val_recall = recall_score(y_val, y_pred_val, zero_division=0)
        val_f1 = f1_score(y_val, y_pred_val, zero_division=0)
        val_auc = roc_auc_score(y_val, y_prob_val)

        mlflow.log_metrics(
            {
                "train_acc": train_acc,
                "val_acc": val_acc,
                "val_precision": val_precision,
                "val_recall": val_recall,
                "val_f1": val_f1,
                "val_auc": val_auc,
            }
        )

        logger.info("──── Results ────")
        logger.info("Train Accuracy : %.4f", train_acc)
        logger.info("Val   Accuracy : %.4f", val_acc)
        logger.info("Val   Precision: %.4f", val_precision)
        logger.info("Val   Recall   : %.4f", val_recall)
        logger.info("Val   F1       : %.4f", val_f1)
        logger.info("Val   AUC      : %.4f", val_auc)
        logger.info("\nValidation classification report:\n%s", classification_report(y_val, y_pred_val))

        # ── Feature importance (top-10) ──────────────────────────────────
        importances = gb.feature_importances_
        feature_names = [f"feat_{i}" for i in range(X_train.shape[1])]
        sorted_idx = np.argsort(importances)[::-1]
        logger.info("Top-10 feature importances:")
        for rank, idx in enumerate(sorted_idx[:10], 1):
            logger.info("  %2d. %s = %.4f", rank, feature_names[idx], importances[idx])

        # ── Save artifacts ───────────────────────────────────────────────
        root = Path(__file__).resolve().parents[3]  # repo root

        model_path = root / "gb_model.joblib"
        preprocessor_path = root / "gb_preprocessor.joblib"

        joblib.dump(calibrated_gb, model_path)
        joblib.dump(preprocessor, preprocessor_path)

        mlflow.log_artifact(str(model_path))
        mlflow.log_artifact(str(preprocessor_path))
        mlflow.sklearn.log_model(calibrated_gb, "gb_model")

        logger.info("Saved model      → %s", model_path)
        logger.info("Saved preprocessor → %s", preprocessor_path)
        logger.info("Training complete ✓")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Gradient Boosting model")
    parser.add_argument("--data_path", type=str, default="data/heart.csv")
    parser.add_argument("--n_estimators", type=int, default=300)
    parser.add_argument("--max_depth", type=int, default=3)
    parser.add_argument("--learning_rate", type=float, default=0.05)
    parser.add_argument("--subsample", type=float, default=0.8)
    parser.add_argument(
        "--imbalance_strategy",
        type=str,
        default="sample_weight",
        choices=["sample_weight", "smote", "none"],
    )
    args = parser.parse_args()

    train(
        data_path=args.data_path,
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
        subsample=args.subsample,
        imbalance_strategy=args.imbalance_strategy,
    )
