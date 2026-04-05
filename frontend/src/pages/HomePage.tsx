import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <Header />
      <main className="container mx-auto px-4 py-16 max-w-4xl tracking-tight">
        <div className="text-center mb-16 animate-in fade-in slide-in-from-bottom-6 duration-700">
          <div className="inline-block p-4 rounded-full bg-blue-50 mb-6">
            <svg className="w-12 h-12 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-600 mb-6">
            Intelligent Risk Prediction
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Unleash the power of machine learning to analyze 18 critical health factors and accurately predict potential cardiovascular risks. 
          </p>
        </div>

        <div className="grid sm:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-150">
          <Link
            to="/assessment"
            className="group block bg-white p-8 rounded-2xl border border-slate-100 shadow-soft hover:shadow-glow hover:-translate-y-1 transition-all duration-300 relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-indigo-50/50 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative">
              <div className="w-12 h-12 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center mb-6">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-slate-800 mb-3">Begin Assessment</h2>
              <p className="text-slate-500 leading-relaxed group-hover:text-slate-600 transition-colors">Start a new evaluation by inputting symptoms, lifestyle traits, and medical history metrics for an instant result.</p>
            </div>
          </Link>

          <div className="flex flex-col gap-6 h-full">
            <Link
              to="/history"
              className="group flex-1 flex flex-col justify-center bg-white p-6 rounded-2xl border border-slate-100 shadow-soft hover:shadow-md hover:border-blue-200 transition-all"
            >
              <h2 className="text-xl font-bold text-slate-800 mb-2 group-hover:text-blue-600 transition-colors">Prediction History</h2>
              <p className="text-sm text-slate-500">Review all your previous cardiovascular health predictions and probability scores.</p>
            </Link>

            <Link
              to="/settings"
              className="group flex-1 flex flex-col justify-center bg-white p-6 rounded-2xl border border-slate-100 shadow-soft hover:shadow-md hover:border-blue-200 transition-all"
            >
              <h2 className="text-xl font-bold text-slate-800 mb-2 group-hover:text-blue-600 transition-colors">Profile Settings</h2>
              <p className="text-sm text-slate-500">Verify and update your age, gender, and biological parameters for the AI model.</p>
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HomePage;
