import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import RiskResult from '../components/RiskResult';
import {
  getApiErrorMessage,
  predictHeartDisease,
  normalizeClinicalInput,
  type ClinicalHeartInput,
  type PredictionResponse,
} from '../services/api';

const AssessmentDashboard: React.FC = () => {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { register, handleSubmit } = useForm<ClinicalHeartInput>({
    defaultValues: {
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
    },
  });

  const onSubmit = async (data: ClinicalHeartInput) => {
    setLoading(true);
    setError(null);
    try {
      const response = await predictHeartDisease(normalizeClinicalInput(data));
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
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const renderSelect = (name: keyof ClinicalHeartInput, label: string) => (
    <div className="flex flex-col">
      <label className="text-sm font-semibold text-slate-700 mb-1">{label}</label>
      <select
        {...register(name, { valueAsNumber: true })}
        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all shadow-sm cursor-pointer"
      >
        <option value={0}>No / False</option>
        <option value={1}>Yes / True</option>
      </select>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-50 font-sans pb-20 px-4">
      <Header />
      <main className="container mx-auto max-w-4xl pt-8">
        <div className="mb-8">
          <Link to="/" className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">
            <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Dashboard
          </Link>
        </div>

        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-600 mb-4 tracking-tight">
            Comprehensive Heart Assessment
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Our AI model analyzes 18 distinct risk factors. Your age and gender are automatically securely sourced from your profile. Please provide accurate insights below for the most precise risk prediction.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded-lg shadow-sm">
            <p className="text-sm text-red-700 font-medium">{error}</p>
          </div>
        )}

        {result ? (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <RiskResult result={result} onReset={handleReset} />
          </div>
        ) : (
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500"
          >
            {/* Section 1: Symptoms */}
            <div className="bg-white p-8 rounded-2xl shadow-soft border border-slate-100">
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold mr-3">
                  1
                </div>
                <h2 className="text-2xl font-bold text-slate-800">Presenting Symptoms</h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {renderSelect('Chest_Pain', 'Chest Pain / Angina')}
                {renderSelect('Shortness_of_Breath', 'Shortness of Breath')}
                {renderSelect('Fatigue', 'Unusual Fatigue')}
                {renderSelect('Palpitations', 'Heart Palpitations')}
                {renderSelect('Dizziness', 'Dizziness / Lightheadedness')}
                {renderSelect('Swelling', 'Ankle/Leg Swelling')}
                {renderSelect('Pain_Arms_Jaw_Back', 'Pain in Arms, Jaw, or Back')}
                {renderSelect('Cold_Sweats_Nausea', 'Cold Sweats or Nausea')}
              </div>
            </div>

            {/* Section 2: Clinical Risk Factors */}
            <div className="bg-white p-8 rounded-2xl shadow-soft border border-slate-100">
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold mr-3">
                  2
                </div>
                <h2 className="text-2xl font-bold text-slate-800">Clinical Risk Factors</h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {renderSelect('High_BP', 'High Blood Pressure (Hypertension)')}
                {renderSelect('High_Cholesterol', 'High Cholesterol')}
                {renderSelect('Diabetes', 'Diabetes')}
                {renderSelect('Obesity', 'Obesity')}
              </div>
            </div>

            {/* Section 3: Lifestyle & Environment */}
            <div className="bg-white p-8 rounded-2xl shadow-soft border border-slate-100">
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center font-bold mr-3">
                  3
                </div>
                <h2 className="text-2xl font-bold text-slate-800">Lifestyle & History</h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {renderSelect('Smoking', 'Current / Former Smoker')}
                {renderSelect('Sedentary_Lifestyle', 'Sedentary Lifestyle')}
                {renderSelect('Family_History', 'Family History of Heart conditions')}
                {renderSelect('Chronic_Stress', 'Chronic Stress')}
              </div>
            </div>

            <div className="flex justify-center pt-6 pb-6 w-full">
              <button
                type="submit"
                disabled={loading}
                className={`group relative flex items-center justify-center px-10 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-lg font-bold rounded-full shadow-glow transition-all transform hover:-translate-y-1 hover:shadow-lg active:translate-y-0 w-full sm:w-auto ${
                  loading ? 'opacity-70 cursor-wait' : ''
                }`}
              >
                {loading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing Risk Factors...
                  </span>
                ) : (
                  'Generate Risk Assessment'
                )}
              </button>
            </div>
          </form>
        )}
      </main>
    </div>
  );
};

export default AssessmentDashboard;
