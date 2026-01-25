from pydantic import BaseModel, Field, ConfigDict

class HeartDiseaseInput(BaseModel):
    Chest_Pain: int = Field(..., description="1 = Yes, 0 = No")
    Shortness_of_Breath: int = Field(..., description="1 = Yes, 0 = No")
    Fatigue: int = Field(..., description="1 = Yes, 0 = No")
    Palpitations: int = Field(..., description="1 = Yes, 0 = No")
    Dizziness: int = Field(..., description="1 = Yes, 0 = No")
    Swelling: int = Field(..., description="1 = Yes, 0 = No")
    Pain_Arms_Jaw_Back: int = Field(..., description="1 = Yes, 0 = No")
    Cold_Sweats_Nausea: int = Field(..., description="1 = Yes, 0 = No")
    High_BP: int = Field(..., description="1 = Yes, 0 = No")
    High_Cholesterol: int = Field(..., description="1 = Yes, 0 = No")
    Diabetes: int = Field(..., description="1 = Yes, 0 = No")
    Smoking: int = Field(..., description="1 = Yes, 0 = No")
    Obesity: int = Field(..., description="1 = Yes, 0 = No")
    Sedentary_Lifestyle: int = Field(..., description="1 = Yes, 0 = No")
    Family_History: int = Field(..., description="1 = Yes, 0 = No")
    Chronic_Stress: int = Field(..., description="1 = Yes, 0 = No")
    Gender: int = Field(..., description="1 = Male, 0 = Female")
    Age: int = Field(..., description="Age in years")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Chest_Pain": 1,
                "Shortness_of_Breath": 0,
                "Fatigue": 1,
                "Palpitations": 0,
                "Dizziness": 0,
                "Swelling": 0,
                "Pain_Arms_Jaw_Back": 1,
                "Cold_Sweats_Nausea": 0,
                "High_BP": 1,
                "High_Cholesterol": 0,
                "Diabetes": 1,
                "Smoking": 0,
                "Obesity": 1,
                "Sedentary_Lifestyle": 1,
                "Family_History": 1,
                "Chronic_Stress": 0,
                "Gender": 1,
                "Age": 55
            }
        }
    )

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 = Healthy, 1 = Heart Disease")
    probability: float = Field(..., description="Probability of Heart Disease")
    risk_level: str = Field(..., description="Low, Moderate, or High Risk")
