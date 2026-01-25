import React from 'react';
import { useForm } from 'react-hook-form';
import type { HeartDiseaseInput } from '../services/api';

interface Props {
  onSubmit: (data: HeartDiseaseInput) => void;
  isLoading: boolean;
}

const PredictionForm: React.FC<Props> = ({ onSubmit, isLoading }) => {
  const { register, handleSubmit, formState: { errors } } = useForm<HeartDiseaseInput>({
    defaultValues: {
      age: 45, sex: 1, cp: 0, trestbps: 120, chol: 200, fbs: 0, 
      restecg: 0, thalach: 150, exang: 0, oldpeak: 0.0, slope: 1, ca: 0, thal: 2
    }
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
      {/* Section 1: Personal Info */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
            <span className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-2 text-sm">1</span>
            Patient Demographics
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Age</label>
                <input {...register("age", { required: true, min: 1, max: 120 })} type="number" className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" />
            </div>
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Sex</label>
                <select {...register("sex", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={1}>Male</option>
                    <option value={0}>Female</option>
                </select>
            </div>
        </div>
      </div>

      {/* Section 2: Clinical Data */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
            <span className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-2 text-sm">2</span>
            Clinical Measurements
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Resting BP (mm Hg)</label>
                <input {...register("trestbps", { valueAsNumber: true })} type="number" className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Cholesterol (mg/dl)</label>
                <input {...register("chol", { valueAsNumber: true })} type="number" className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Max Heart Rate</label>
                <input {...register("thalach", { valueAsNumber: true })} type="number" className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
             <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Chest Pain Type</label>
                 <select {...register("cp", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={0}>Typical Angina</option>
                    <option value={1}>Atypical Angina</option>
                    <option value={2}>Non-anginal Pain</option>
                    <option value={3}>Asymptomatic</option>
                </select>
            </div>
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Fasting Blood Sugar ({'>'}120)</label>
                 <select {...register("fbs", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={0}>False</option>
                    <option value={1}>True</option>
                </select>
            </div>
             <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Rest ECG</label>
                 <select {...register("restecg", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={0}>Normal</option>
                    <option value={1}>ST-T Wave Abnormality</option>
                    <option value={2}>Left Ventricular Hypertrophy</option>
                </select>
            </div>
        </div>
      </div>

       {/* Section 3: Advanced Cardiac */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
            <span className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-2 text-sm">3</span>
            Stress Test & Angiography
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Exercise Induced Angina</label>
                 <select {...register("exang", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={0}>No</option>
                    <option value={1}>Yes</option>
                </select>
            </div>
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">ST Depression (Oldpeak)</label>
                <input {...register("oldpeak", { valueAsNumber: true })} type="number" step="0.1" className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Slope of Peak Exercise ST</label>
                 <select {...register("slope", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={0}>Upsloping</option>
                    <option value={1}>Flat</option>
                    <option value={2}>Downsloping</option>
                </select>
            </div>
             <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Major Vessels (CA)</label>
                 <select {...register("ca", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={0}>0</option>
                    <option value={1}>1</option>
                    <option value={2}>2</option>
                    <option value={3}>3</option>
                </select>
            </div>
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Thalassemia</label>
                 <select {...register("thal", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={1}>Normal</option>
                    <option value={2}>Fixed Defect</option>
                    <option value={3}>Reversible Defect</option>
                </select>
            </div>
        </div>
      </div>

      <div className="flex justify-end pt-4">
        <button 
            type="submit" 
            disabled={isLoading}
            className={`px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg shadow-lg shadow-blue-200 transition-all transform hover:-translate-y-0.5 active:translate-y-0 ${isLoading ? 'opacity-70 cursor-wait' : ''}`}
        >
            {isLoading ? 'Processing Analysis...' : 'Generate Prediction'}
        </button>
      </div>
    </form>
  );
};

export default PredictionForm;
