from fastapi import APIRouter, HTTPException, Depends
from src.heart_disease.api.v1.schemas import HeartDiseaseInput, PredictionResponse
from src.heart_disease.ml.predict import get_predictor, HeartDiseasePredictor
from src.heart_disease.core.config import get_settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency for Predictor
# We use a singleton-like pattern via lru_cache or module level var in real apps
# Here, we instantiate/get it.
# In production, initialize this in startup event to avoid loading per request if generic.
_predictor = None

def get_model_predictor():
    global _predictor
    if _predictor is None:
        settings = get_settings()
        try:
            _predictor = get_predictor(settings.MODEL_DIR)
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            # Identify if it's because model missing
            raise HTTPException(status_code=503, detail="Model not loaded or available.")
    return _predictor

@router.post("/predict", response_model=PredictionResponse)
async def predict_heart_disease(
    input_data: HeartDiseaseInput,
    predictor: HeartDiseasePredictor = Depends(get_model_predictor)
):
    try:
        data_dict = input_data.model_dump()
        prob = predictor.predict(data_dict)
        
        prediction = 1 if prob > 0.5 else 0
        
        risk_level = "Low"
        if prob > 0.7:
            risk_level = "High"
        elif prob > 0.35: # Conservative threshold
            risk_level = "Moderate"
            
        return PredictionResponse(
            prediction=prediction,
            probability=round(prob, 4),
            risk_level=risk_level
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
