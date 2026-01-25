import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export interface HeartDiseaseInput {
  Chest_Pain: number;
  Shortness_of_Breath: number;
  Fatigue: number;
  Palpitations: number;
  Dizziness: number;
  Swelling: number;
  Pain_Arms_Jaw_Back: number;
  Cold_Sweats_Nausea: number;
  High_BP: number;
  High_Cholesterol: number;
  Diabetes: number;
  Smoking: number;
  Obesity: number;
  Sedentary_Lifestyle: number;
  Family_History: number;
  Chronic_Stress: number;
  Gender: number;
  Age: number;
}

export interface PredictionResponse {
  prediction: number;
  probability: number;
  risk_level: string;
}

export const predictHeartDisease = async (data: HeartDiseaseInput): Promise<PredictionResponse> => {
  const response = await axios.post<PredictionResponse>(`${API_URL}/predict`, data);
  return response.data;
};
