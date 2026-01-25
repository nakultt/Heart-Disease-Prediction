import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export interface HeartDiseaseInput {
  age: number;
  sex: number;
  cp: number;
  trestbps: number;
  chol: number;
  fbs: number;
  restecg: number;
  thalach: number;
  exang: number;
  oldpeak: number;
  slope: number;
  ca: number;
  thal: number;
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
