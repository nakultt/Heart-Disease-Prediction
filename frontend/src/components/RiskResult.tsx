import React from 'react';
import type { PredictionResponse } from '../services/api';

interface Props {
  result: PredictionResponse;
  onReset: () => void;
}

const RiskResult: React.FC<Props> = ({ result, onReset }) => {
  const isHighRisk = result.prediction === 1;
  const percentage = Math.round(result.probability * 100);
  
  // Dynamic colors based on risk
  const bgColor = isHighRisk ? 'bg-red-50' : 'bg-emerald-50';
  const textColor = isHighRisk ? 'text-red-800' : 'text-emerald-800';
  const borderColor = isHighRisk ? 'border-red-200' : 'border-emerald-200';
  const progressColor = isHighRisk ? 'bg-red-500' : 'bg-emerald-500';

  return (
    <div className={`mt-8 p-8 rounded-2xl border-2 ${borderColor} ${bgColor} shadow-xl transition-all duration-500 animate-fade-in`}>
      <div className="text-center">
        <h2 className={`text-3xl font-bold ${textColor} mb-2`}>
          {isHighRisk ? 'High Risk Detected' : 'Low Risk Assessment'}
        </h2>
        <p className="text-slate-600 mb-6">Based on the provided clinical data</p>
        
        <div className="relative pt-4 pb-8 flex justify-center">
            {/* Simple Gauge Visualization */}
            <div className="w-64 bg-slate-200 rounded-full h-4 relative overflow-hidden">
                <div 
                    className={`${progressColor} h-full rounded-full transition-all duration-1000 ease-out`}
                    style={{ width: `${percentage}%` }}
                ></div>
            </div>
        </div>
        
        <div className="text-5xl font-extrabold text-slate-800 mb-2">
            {percentage}%
        </div>
        <div className="text-sm font-semibold text-slate-500 uppercase tracking-widest mb-8">
            Probability
        </div>

        <div className="flex justify-center space-x-4">
            <button 
                onClick={onReset}
                className="px-6 py-3 bg-white border border-slate-300 text-slate-700 font-semibold rounded-lg hover:bg-slate-50 transition shadow-sm"
            >
                New Assessment
            </button>
            {isHighRisk && (
                <button className="px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition shadow-lg shadow-red-200">
                    Consult Cardiologist
                </button>
            )}
        </div>
      </div>
    </div>
  );
};

export default RiskResult;
