import React, { useState } from 'react';
import Header from '../components/Header';
import PredictionForm from '../components/PredictionForm';
import RiskResult from '../components/RiskResult';
import { predictHeartDisease } from '../services/api';
import type { HeartDiseaseInput, PredictionResponse } from '../services/api';

/**
 * Main assessment UI — only reachable when ProtectedRoute confirms a JWT exists.
 */
const PredictionPage: React.FC = () => {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePrediction = async (data: HeartDiseaseInput) => {
    setLoading(true);
    setError(null);
    try {
      const response = await predictHeartDisease(data);
      setResult(response);
    } catch (err) {
      console.error(err);
      setError(
        'Failed to get a prediction. Check that the backend is running and you are still logged in.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <Header />

      <main className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-slate-900 mb-4 tracking-tight">
            Heart Disease Risk Assessment
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Advanced machine learning analysis using 13 clinical markers to predict cardiac health
            risks with high precision.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded shadow-sm">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {result ? (
          <RiskResult result={result} onReset={handleReset} />
        ) : (
          <div className="animate-fade-in-up">
            <PredictionForm onSubmit={handlePrediction} isLoading={loading} />
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-slate-200 mt-20 py-8">
        <div className="container mx-auto px-6 text-center text-slate-500 text-sm">
          &copy; {new Date().getFullYear()} CardioGuard AI System. For research and educational
          purposes only.
        </div>
      </footer>
    </div>
  );
};

export default PredictionPage;
