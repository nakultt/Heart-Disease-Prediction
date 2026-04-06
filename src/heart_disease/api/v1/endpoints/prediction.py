from fastapi import APIRouter, Depends, HTTPException
from src.heart_disease.api.v1.schemas import (
    ClinicalHeartInput,
    HeartDiseaseInput,
    PredictionResponse,
)
from src.heart_disease.auth.dependencies import get_current_user_record
from src.heart_disease.db import predictions_repo, users_repo
from src.heart_disease.ml.predict import get_predictor, HeartDiseasePredictor
from src.heart_disease.core.config import get_settings
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
        
        # Determine Gender numeric representation (Dataset Gender: 0.0 or 1.0)
        # We can map it if 1=male, 0=female
        gender_str = str(user["gender"]).lower()
        if gender_str == "male":
            gender_val = 1.0
        else:
            gender_val = 0.0
            
        full_dict = {
            "Chest_Pain": float(clinical_dict["Chest_Pain"]),
            "Shortness_of_Breath": float(clinical_dict["Shortness_of_Breath"]),
            "Fatigue": float(clinical_dict["Fatigue"]),
            "Palpitations": float(clinical_dict["Palpitations"]),
            "Dizziness": float(clinical_dict["Dizziness"]),
            "Swelling": float(clinical_dict["Swelling"]),
            "Pain_Arms_Jaw_Back": float(clinical_dict["Pain_Arms_Jaw_Back"]),
            "Cold_Sweats_Nausea": float(clinical_dict["Cold_Sweats_Nausea"]),
            "High_BP": float(clinical_dict["High_BP"]),
            "High_Cholesterol": float(clinical_dict["High_Cholesterol"]),
            "Diabetes": float(clinical_dict["Diabetes"]),
            "Smoking": float(clinical_dict["Smoking"]),
            "Obesity": float(clinical_dict["Obesity"]),
            "Sedentary_Lifestyle": float(clinical_dict["Sedentary_Lifestyle"]),
            "Family_History": float(clinical_dict["Family_History"]),
            "Chronic_Stress": float(clinical_dict["Chronic_Stress"]),
            "Gender": gender_val,
            "Age": float(user["age"])
        }
        
        heart_input = HeartDiseaseInput(**full_dict)
        data_dict = heart_input.model_dump()

        logger.info("Running prediction using [%s] model for user: %s", get_settings().MODEL_TYPE.upper(), current_user)
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
