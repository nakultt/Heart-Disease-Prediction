import React from 'react';
import { useForm } from 'react-hook-form';
import type { HeartDiseaseInput } from '../services/api';

interface Props {
  onSubmit: (data: HeartDiseaseInput) => void;
  isLoading: boolean;
}

const BinarySelect = ({ label, register, name }: { label: string, register: any, name: keyof HeartDiseaseInput }) => (
    <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">{label}</label>
        <select {...register(name, { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
        </select>
    </div>
);

const PredictionForm: React.FC<Props> = ({ onSubmit, isLoading }) => {
  const { register, handleSubmit } = useForm<HeartDiseaseInput>({
    defaultValues: {
      Age: 45, Gender: 1, Chest_Pain: 0, Shortness_of_Breath: 0, Fatigue: 0,
      Palpitations: 0, Dizziness: 0, Swelling: 0, Pain_Arms_Jaw_Back: 0,
      Cold_Sweats_Nausea: 0, High_BP: 0, High_Cholesterol: 0, Diabetes: 0,
      Smoking: 0, Obesity: 0, Sedentary_Lifestyle: 0, Family_History: 0,
      Chronic_Stress: 0
    }
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
      {/* Section 1: Demographics & Lifestyle */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
            <span className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-2 text-sm">1</span>
            Demographics & Lifestyle
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Age</label>
                <input {...register("Age", { required: true, min: 1, max: 120 })} type="number" className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Gender</label>
                <select {...register("Gender", { valueAsNumber: true })} className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value={1}>Male</option>
                    <option value={0}>Female</option>
                </select>
            </div>
            <BinarySelect label="Family History" register={register} name="Family_History" />
            <BinarySelect label="Smoking" register={register} name="Smoking" />
            <BinarySelect label="Obesity" register={register} name="Obesity" />
            <BinarySelect label="Sedentary Lifestyle" register={register} name="Sedentary_Lifestyle" />
            <BinarySelect label="High Blood Pressure" register={register} name="High_BP" />
            <BinarySelect label="High Cholesterol" register={register} name="High_Cholesterol" />
            <BinarySelect label="Diabetes" register={register} name="Diabetes" />
        </div>
      </div>

      {/* Section 2: Symptoms */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
            <span className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-2 text-sm">2</span>
            Symptoms & Conditions
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <BinarySelect label="Chest Pain" register={register} name="Chest_Pain" />
            <BinarySelect label="Shortness of Breath" register={register} name="Shortness_of_Breath" />
            <BinarySelect label="Fatigue" register={register} name="Fatigue" />
            <BinarySelect label="Palpitations" register={register} name="Palpitations" />
            <BinarySelect label="Dizziness" register={register} name="Dizziness" />
            <BinarySelect label="Swelling / Edema" register={register} name="Swelling" />
            <BinarySelect label="Pain in Arms/Jaw/Back" register={register} name="Pain_Arms_Jaw_Back" />
            <BinarySelect label="Cold Sweats / Nausea" register={register} name="Cold_Sweats_Nausea" />
            <BinarySelect label="Chronic Stress" register={register} name="Chronic_Stress" />
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
