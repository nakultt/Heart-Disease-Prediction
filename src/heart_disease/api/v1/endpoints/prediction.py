from fastapi import APIRouter, Depends, HTTPException
from src.heart_disease.api.v1.schemas import (
    ClinicalHeartInput,
    HeartDiseaseInput,
    PredictionResponse,
)
from src.heart_disease.auth.dependencies import get_current_user_record
from src.heart_disease.db import predictions_repo, users_repo
from src.heart_disease.ml.predict import get_predictor, HeartDiseasePredictor
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

_predictor = None


def get_model_predictor():
    global _predictor
    if _predictor is None:
        try:
            # Artifacts resolved vs repo root so cwd (e.g. frontend/) does not break loading.
            _predictor = get_predictor()
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Ensure best_model.pth and preprocessor.joblib exist in the project root.",
            )
    return _predictor


@router.post("/predict", response_model=PredictionResponse)
async def predict_heart_disease(
    input_data: ClinicalHeartInput,
    predictor: HeartDiseasePredictor = Depends(get_model_predictor),
    user: dict = Depends(get_current_user_record),
):
    """
    Run the model using clinical fields from the body plus age/sex from the user's MongoDB profile.
    Stores each run in prediction history.
    """
    current_user = str(user["username"])
    try:
        clinical_dict = input_data.model_dump()
        # MongoDB may return BSON numeric types; sklearn / pandas need plain Python numbers.
        full_dict = {
            "age": int(user["age"]),
            "sex": int(users_repo.gender_to_sex(str(user["gender"]))),
            "cp": int(clinical_dict["cp"]),
            "trestbps": int(clinical_dict["trestbps"]),
            "chol": int(clinical_dict["chol"]),
            "fbs": int(clinical_dict["fbs"]),
            "restecg": int(clinical_dict["restecg"]),
            "thalach": int(clinical_dict["thalach"]),
            "exang": int(clinical_dict["exang"]),
            "oldpeak": float(clinical_dict["oldpeak"]),
            "slope": int(clinical_dict["slope"]),
            "ca": int(clinical_dict["ca"]),
            "thal": int(clinical_dict["thal"]),
        }
        heart_input = HeartDiseaseInput(**full_dict)
        data_dict = heart_input.model_dump()

        logger.debug("Prediction request for authenticated user: %s", current_user)
        prob = predictor.predict(data_dict)

        prediction = 1 if prob > 0.5 else 0

        risk_level = "Low"
        if prob > 0.7:
            risk_level = "High"
        elif prob > 0.35:
            risk_level = "Moderate"

        try:
            predictions_repo.insert_history(
                username=current_user,
                clinical_input=clinical_dict,
                full_model_input=data_dict,
                prediction=prediction,
                probability=round(prob, 4),
                risk_level=risk_level,
            )
        except Exception as hist_e:
            logger.warning("Prediction saved but history insert failed: %s", hist_e)

        return PredictionResponse(
            prediction=prediction,
            probability=round(prob, 4),
            risk_level=risk_level,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
