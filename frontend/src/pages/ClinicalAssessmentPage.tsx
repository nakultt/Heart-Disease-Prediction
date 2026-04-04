import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import PredictionForm from '../components/PredictionForm';
import RiskResult from '../components/RiskResult';
import { getApiErrorMessage, predictHeartDisease } from '../services/api';
import type { ClinicalHeartInput, PredictionResponse } from '../services/api';

const ClinicalAssessmentPage: React.FC = () => {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePrediction = async (data: ClinicalHeartInput) => {
    setLoading(true);
    setError(null);
    try {
      const response = await predictHeartDisease(data);
      setResult(response);
    } catch (err) {
      console.error(err);
      setError(getApiErrorMessage(err));
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
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-6">
          <Link to="/" className="text-sm text-blue-600 hover:underline">
            ← Back to home
          </Link>
        </div>
        <div className="text-center mb-10">
          <h1 className="text-3xl font-extrabold text-slate-900 mb-2">Clinical measurements</h1>
          <p className="text-slate-600">
            Risk model uses your profile age/gender plus the values below. Each run is saved to History.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded shadow-sm">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {result ? (
          <RiskResult result={result} onReset={handleReset} />
        ) : (
          <PredictionForm onSubmit={handlePrediction} isLoading={loading} />
        )}
      </main>
    </div>
  );
};

export default ClinicalAssessmentPage;
