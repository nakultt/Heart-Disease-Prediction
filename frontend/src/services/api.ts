import axios, { isAxiosError } from 'axios';

export const TOKEN_STORAGE_KEY = 'heart_disease_jwt';

/**
 * Resolve API origin on each use so it stays correct if Vite switches ports (5173 → 5174).
 */
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

/** Defaults match PredictionForm — used when a number input was cleared (NaN → JSON null). */
const CLINICAL_DEFAULTS: ClinicalHeartInput = {
  cp: 0,
  trestbps: 120,
  chol: 200,
  fbs: 0,
  restecg: 0,
  thalach: 150,
  exang: 0,
  oldpeak: 0,
  slope: 1,
  ca: 0,
  thal: 2,
};

function asInt(v: unknown, fallback: number): number {
  if (typeof v === 'number' && Number.isFinite(v)) return Math.trunc(v);
  if (typeof v === 'string' && v.trim() !== '') {
    const n = parseInt(v, 10);
    if (Number.isFinite(n)) return n;
  }
  return fallback;
}

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
    cp: asInt(data.cp, CLINICAL_DEFAULTS.cp),
    trestbps: asInt(data.trestbps, CLINICAL_DEFAULTS.trestbps),
    chol: asInt(data.chol, CLINICAL_DEFAULTS.chol),
    fbs: asInt(data.fbs, CLINICAL_DEFAULTS.fbs),
    restecg: asInt(data.restecg, CLINICAL_DEFAULTS.restecg),
    thalach: asInt(data.thalach, CLINICAL_DEFAULTS.thalach),
    exang: asInt(data.exang, CLINICAL_DEFAULTS.exang),
    oldpeak: asFloat(data.oldpeak, CLINICAL_DEFAULTS.oldpeak),
    slope: asInt(data.slope, CLINICAL_DEFAULTS.slope),
    ca: asInt(data.ca, CLINICAL_DEFAULTS.ca),
    thal: asInt(data.thal, CLINICAL_DEFAULTS.thal),
  };
}

/** Clinical fields only — age/sex are taken from the user profile on the server. */
export interface ClinicalHeartInput {
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

/** Human-readable message for axios / network failures (use in catch blocks). */
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
