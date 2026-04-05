from pydantic import BaseModel, Field, ConfigDict

class HeartDiseaseInput(BaseModel):
    # Age and Gender from User Profile
    Age: float = Field(..., description="Age in years")
    Gender: float = Field(..., description="0 = female, 1 = male")
    
    # Clinical inputs from UI
    Chest_Pain: float = Field(..., description="0 = False, 1 = True")
    Shortness_of_Breath: float = Field(..., description="0 = False, 1 = True")
    Fatigue: float = Field(..., description="0 = False, 1 = True")
    Palpitations: float = Field(..., description="0 = False, 1 = True")
    Dizziness: float = Field(..., description="0 = False, 1 = True")
    Swelling: float = Field(..., description="0 = False, 1 = True")
    Pain_Arms_Jaw_Back: float = Field(..., description="0 = False, 1 = True")
    Cold_Sweats_Nausea: float = Field(..., description="0 = False, 1 = True")
    High_BP: float = Field(..., description="0 = False, 1 = True")
    High_Cholesterol: float = Field(..., description="0 = False, 1 = True")
    Diabetes: float = Field(..., description="0 = False, 1 = True")
    Smoking: float = Field(..., description="0 = False, 1 = True")
    Obesity: float = Field(..., description="0 = False, 1 = True")
    Sedentary_Lifestyle: float = Field(..., description="0 = False, 1 = True")
    Family_History: float = Field(..., description="0 = False, 1 = True")
    Chronic_Stress: float = Field(..., description="0 = False, 1 = True")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Chest_Pain": 0.0,
                "Shortness_of_Breath": 0.0,
                "Fatigue": 0.0,
                "Palpitations": 1.0,
                "Dizziness": 0.0,
                "Swelling": 0.0,
                "Pain_Arms_Jaw_Back": 0.0,
                "Cold_Sweats_Nausea": 0.0,
                "High_BP": 0.0,
                "High_Cholesterol": 0.0,
                "Diabetes": 0.0,
                "Smoking": 1.0,
                "Obesity": 0.0,
                "Sedentary_Lifestyle": 1.0,
                "Family_History": 0.0,
                "Chronic_Stress": 0.0,
                "Gender": 0.0,
                "Age": 48.0
            }
        }
    )

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 = Healthy, 1 = Heart Disease")
    probability: float = Field(..., description="Probability of Heart Disease")
    risk_level: str = Field(..., description="Low, Moderate, or High Risk")


class ClinicalHeartInput(BaseModel):
    """
    Clinical features only. Age and Gender come from the logged-in user's MongoDB profile.
    """
    Chest_Pain: float = Field(..., description="0 = False, 1 = True")
    Shortness_of_Breath: float = Field(..., description="0 = False, 1 = True")
    Fatigue: float = Field(..., description="0 = False, 1 = True")
    Palpitations: float = Field(..., description="0 = False, 1 = True")
    Dizziness: float = Field(..., description="0 = False, 1 = True")
    Swelling: float = Field(..., description="0 = False, 1 = True")
    Pain_Arms_Jaw_Back: float = Field(..., description="0 = False, 1 = True")
    Cold_Sweats_Nausea: float = Field(..., description="0 = False, 1 = True")
    High_BP: float = Field(..., description="0 = False, 1 = True")
    High_Cholesterol: float = Field(..., description="0 = False, 1 = True")
    Diabetes: float = Field(..., description="0 = False, 1 = True")
    Smoking: float = Field(..., description="0 = False, 1 = True")
    Obesity: float = Field(..., description="0 = False, 1 = True")
    Sedentary_Lifestyle: float = Field(..., description="0 = False, 1 = True")
    Family_History: float = Field(..., description="0 = False, 1 = True")
    Chronic_Stress: float = Field(..., description="0 = False, 1 = True")
