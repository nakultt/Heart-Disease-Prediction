import axios, { isAxiosError } from 'axios';

export const TOKEN_STORAGE_KEY = 'heart_disease_jwt';

export function resolveApiBase(): string {
  const fromEnv = import.meta.env.VITE_API_BASE_URL?.trim();
  if (fromEnv) {
    return fromEnv.replace(/\/+$/, '');
  }
  if (import.meta.env.DEV && typeof window !== 'undefined') {
    return window.location.origin;
  }
  if (import.meta.env.DEV) {
    return 'http://localhost:5173';
  }
  return 'http://localhost:8000';
}

const apiPath = (p: string) => (p.startsWith('/') ? p : `/${p}`);

export const apiClient = axios.create();

apiClient.interceptors.request.use((config) => {
  config.baseURL = resolveApiBase();
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (isAxiosError(error) && error.response?.status === 401) {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      if (!window.location.pathname.startsWith('/login')) {
        window.location.assign('/login');
      }
    }
    return Promise.reject(error);
  }
);

/** Defaults for the PredictionForm — used as safety fallback. */
const CLINICAL_DEFAULTS: ClinicalHeartInput = {
  Chest_Pain: 0,
  Shortness_of_Breath: 0,
  Fatigue: 0,
  Palpitations: 0,
  Dizziness: 0,
  Swelling: 0,
  Pain_Arms_Jaw_Back: 0,
  Cold_Sweats_Nausea: 0,
  High_BP: 0,
  High_Cholesterol: 0,
  Diabetes: 0,
  Smoking: 0,
  Obesity: 0,
  Sedentary_Lifestyle: 0,
  Family_History: 0,
  Chronic_Stress: 0,
};

function asFloat(v: unknown, fallback: number): number {
  if (typeof v === 'number' && Number.isFinite(v)) return v;
  if (typeof v === 'string' && v.trim() !== '') {
    const n = parseFloat(v);
    if (Number.isFinite(n)) return n;
  }
  return fallback;
}

/** Coerce react-hook-form values so empty number fields never become null/NaN in JSON. */
export function normalizeClinicalInput(data: Partial<ClinicalHeartInput>): ClinicalHeartInput {
  return {
    Chest_Pain: asFloat(data.Chest_Pain, CLINICAL_DEFAULTS.Chest_Pain),
    Shortness_of_Breath: asFloat(data.Shortness_of_Breath, CLINICAL_DEFAULTS.Shortness_of_Breath),
    Fatigue: asFloat(data.Fatigue, CLINICAL_DEFAULTS.Fatigue),
    Palpitations: asFloat(data.Palpitations, CLINICAL_DEFAULTS.Palpitations),
    Dizziness: asFloat(data.Dizziness, CLINICAL_DEFAULTS.Dizziness),
    Swelling: asFloat(data.Swelling, CLINICAL_DEFAULTS.Swelling),
    Pain_Arms_Jaw_Back: asFloat(data.Pain_Arms_Jaw_Back, CLINICAL_DEFAULTS.Pain_Arms_Jaw_Back),
    Cold_Sweats_Nausea: asFloat(data.Cold_Sweats_Nausea, CLINICAL_DEFAULTS.Cold_Sweats_Nausea),
    High_BP: asFloat(data.High_BP, CLINICAL_DEFAULTS.High_BP),
    High_Cholesterol: asFloat(data.High_Cholesterol, CLINICAL_DEFAULTS.High_Cholesterol),
    Diabetes: asFloat(data.Diabetes, CLINICAL_DEFAULTS.Diabetes),
    Smoking: asFloat(data.Smoking, CLINICAL_DEFAULTS.Smoking),
    Obesity: asFloat(data.Obesity, CLINICAL_DEFAULTS.Obesity),
    Sedentary_Lifestyle: asFloat(data.Sedentary_Lifestyle, CLINICAL_DEFAULTS.Sedentary_Lifestyle),
    Family_History: asFloat(data.Family_History, CLINICAL_DEFAULTS.Family_History),
    Chronic_Stress: asFloat(data.Chronic_Stress, CLINICAL_DEFAULTS.Chronic_Stress),
  };
}

/** Clinical fields only — Age/Gender are taken from the user profile on the server. */
export interface ClinicalHeartInput {
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
}

export interface PredictionResponse {
  prediction: number;
  probability: number;
  risk_level: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export type Gender = 'male' | 'female' | 'other';

export interface RegisterPayload {
  username: string;
  password: string;
  age: number;
  gender: Gender;
  weight_kg: number;
  height_cm: number;
}

export interface UserProfile {
  username: string;
  age: number;
  gender: string;
  weight_kg: number;
  height_cm: number;
  smoking: string;
  stress: string;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface PredictionHistoryItem {
  id: string;
  created_at: string | null;
  prediction: number;
  probability: number;
  risk_level: string;
  clinical_input?: Record<string, number> | null;
}

export const predictHeartDisease = async (
  data: ClinicalHeartInput
): Promise<PredictionResponse> => {
  const response = await apiClient.post<PredictionResponse>(apiPath('/api/v1/predict'), data);
  return response.data;
};

export const loginRequest = async (username: string, password: string): Promise<TokenResponse> => {
  const response = await axios.post<TokenResponse>(`${resolveApiBase()}/auth/login`, {
    username,
    password,
  });
  return response.data;
};

export const registerRequest = async (
  payload: RegisterPayload
): Promise<UserProfile & { message: string }> => {
  const response = await axios.post<UserProfile & { message: string }>(
    `${resolveApiBase()}/auth/register`,
    payload
  );
  return response.data;
};

export const fetchMyProfile = async (): Promise<UserProfile> => {
  const response = await apiClient.get<UserProfile>(apiPath('/api/v1/me'));
  return response.data;
};

export const updateMyProfile = async (patch: Partial<UserProfile>): Promise<UserProfile> => {
  const body: Record<string, unknown> = {};
  if (patch.age !== undefined) body.age = patch.age;
  if (patch.gender !== undefined) body.gender = patch.gender;
  if (patch.weight_kg !== undefined) body.weight_kg = patch.weight_kg;
  if (patch.height_cm !== undefined) body.height_cm = patch.height_cm;
  if (patch.smoking !== undefined) body.smoking = patch.smoking;
  if (patch.stress !== undefined) body.stress = patch.stress;
  const response = await apiClient.patch<UserProfile>(apiPath('/api/v1/profile'), body);
  return response.data;
};

export const fetchPredictionHistory = async (): Promise<PredictionHistoryItem[]> => {
  const response = await apiClient.get<PredictionHistoryItem[]>(
    apiPath('/api/v1/predictions/history')
  );
  return response.data;
};

export function getApiErrorMessage(err: unknown): string {
  if (isAxiosError(err)) {
    const d = err.response?.data as { detail?: unknown } | undefined;
    if (d?.detail !== undefined) {
      const det = d.detail;
      if (typeof det === 'string') return det;
      if (Array.isArray(det)) {
        return det
          .map((x: { msg?: string; type?: string }) => x.msg || JSON.stringify(x))
          .join('; ');
      }
    }
    if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
      return 'Cannot reach the API. Start the backend: uvicorn on port 8000 (from the project root), then open the app from the Vite URL (e.g. http://localhost:5173).';
    }
    if (err.response?.status === 503) {
      const detail = (err.response?.data as { detail?: string } | undefined)?.detail;
      return (
        (typeof detail === 'string' && detail) ||
        'Service unavailable (model or database). Check server logs.'
      );
    }
    return err.message || 'Request failed';
  }
  if (err instanceof Error) return err.message;
  return 'Something went wrong';
}
