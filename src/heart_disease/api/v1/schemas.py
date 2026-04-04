from pydantic import BaseModel, Field, ConfigDict

class HeartDiseaseInput(BaseModel):
    age: int = Field(..., example=63, description="Age in years")
    sex: int = Field(..., example=1, description="1 = male; 0 = female")
    cp: int = Field(..., example=3, description="Chest pain type (0-3)")
    trestbps: int = Field(..., example=145, description="Resting blood pressure (mm Hg)")
    chol: int = Field(..., example=233, description="Serum cholestoral in mg/dl")
    fbs: int = Field(..., example=1, description="Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)")
    restecg: int = Field(..., example=0, description="Resting electrocardiographic results (0-2)")
    thalach: int = Field(..., example=150, description="Maximum heart rate achieved")
    exang: int = Field(..., example=0, description="Exercise induced angina (1 = yes; 0 = no)")
    oldpeak: float = Field(..., example=2.3, description="ST depression induced by exercise relative to rest")
    slope: int = Field(..., example=0, description="Slope of the peak exercise ST segment (0-2)")
    ca: int = Field(..., example=0, description="Number of major vessels (0-3) colored by flourosopy")
    thal: int = Field(..., example=1, description="Thal (1 = normal; 2 = fixed defect; 3 = reversable defect)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145,
                "chol": 233,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 0,
                "ca": 0,
                "thal": 1
            }
        }
    )

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 = Healthy, 1 = Heart Disease")
    probability: float = Field(..., description="Probability of Heart Disease")
    risk_level: str = Field(..., description="Low, Moderate, or High Risk")


class ClinicalHeartInput(BaseModel):
    """
    Clinical features only. Age and sex come from the logged-in user's MongoDB profile.
    """

    cp: int = Field(..., description="Chest pain type (0-3)")
    trestbps: int = Field(..., description="Resting blood pressure (mm Hg)")
    chol: int = Field(..., description="Serum cholesterol in mg/dl")
    fbs: int = Field(..., description="Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)")
    restecg: int = Field(..., description="Resting ECG results (0-2)")
    thalach: int = Field(..., description="Maximum heart rate achieved")
    exang: int = Field(..., description="Exercise induced angina (1 = yes; 0 = no)")
    oldpeak: float = Field(..., description="ST depression (oldpeak)")
    slope: int = Field(..., description="Slope of peak exercise ST (0-2)")
    ca: int = Field(..., description="Number of major vessels (0-3)")
    thal: int = Field(..., description="Thal (1–3 per dataset coding)")
