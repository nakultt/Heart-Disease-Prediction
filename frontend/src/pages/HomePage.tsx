import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';

const cards: { to: string; title: string; desc: string }[] = [
  {
    to: '/demographics',
    title: 'Patient demographics',
    desc: 'Update smoking status and related lifestyle fields.',
  },
  {
    to: '/clinical',
    title: 'Clinical measurements',
    desc: 'Enter lab and cardiac test values for risk prediction.',
  },
  {
    to: '/stress',
    title: 'Stress level',
    desc: 'Record how stressed you feel — updated anytime.',
  },
  {
    to: '/history',
    title: 'History',
    desc: 'Review past predictions saved to your account.',
  },
  {
    to: '/settings',
    title: 'Settings',
    desc: 'Edit age, gender, weight, and height.',
  },
];

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <Header />
      <main className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-slate-900 mb-3 tracking-tight">Home</h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Choose a section. Age and gender are stored from registration and edited only in Settings.
          </p>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          {cards.map((c) => (
            <Link
              key={c.to}
              to={c.to}
              className="block bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:border-blue-300 hover:shadow-md transition"
            >
              <h2 className="text-lg font-semibold text-slate-900 mb-2">{c.title}</h2>
              <p className="text-sm text-slate-600">{c.desc}</p>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
};

export default HomePage;
