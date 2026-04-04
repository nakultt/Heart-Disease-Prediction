import axios, { isAxiosError } from 'axios';

/**
 * Base URL for the FastAPI server.
 * - Dev: empty string → same origin as Vite; `vite.config.ts` proxies /auth and /api to port 8000.
 * - Prod / preview: full URL unless you set VITE_API_BASE_URL in .env.
 */
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.trim() ||
  (import.meta.env.DEV ? '' : 'http://localhost:8000');

/** Key used in localStorage for the JWT (must match AuthContext). */
export const TOKEN_STORAGE_KEY = 'heart_disease_jwt';

const API_V1 = API_BASE_URL ? `${API_BASE_URL}/api/v1` : '/api/v1';

/**
 * Axios instance for routes that need Authorization: Bearer <token>.
 * Login/register use plain axios so no stale token is attached.
 */
export const apiClient = axios.create({
  baseURL: API_BASE_URL || undefined,
});

// Attach JWT from localStorage on every protected request.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// If the token expired or was revoked, clear storage and go back to login.
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

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

/** Call the ML endpoint; apiClient adds the Bearer token automatically. */
export const predictHeartDisease = async (data: HeartDiseaseInput): Promise<PredictionResponse> => {
  const response = await apiClient.post<PredictionResponse>(`${API_V1}/predict`, data);
  return response.data;
};

/** Public: no Authorization header. */
export const loginRequest = async (username: string, password: string): Promise<TokenResponse> => {
  const response = await axios.post<TokenResponse>(`${API_BASE_URL}/auth/login`, {
    username,
    password,
  });
  return response.data;
};

/** Public: no Authorization header. */
export const registerRequest = async (
  username: string,
  password: string
): Promise<{ username: string; message: string }> => {
  const response = await axios.post(`${API_BASE_URL}/auth/register`, { username, password });
  return response.data;
};
