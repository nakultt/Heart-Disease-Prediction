import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import { fetchMyProfile, getApiErrorMessage, updateMyProfile, type Gender } from '../services/api';

const SettingsPage: React.FC = () => {
  const [age, setAge] = useState(30);
  const [gender, setGender] = useState<Gender>('male');
  const [weightKg, setWeightKg] = useState(70);
  const [heightCm, setHeightCm] = useState(170);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const p = await fetchMyProfile();
        if (!cancelled) {
          setAge(p.age);
          setGender((p.gender as Gender) || 'other');
          setWeightKg(p.weight_kg);
          setHeightCm(p.height_cm);
        }
      } catch (e) {
        if (!cancelled) setError(getApiErrorMessage(e));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    setError(null);
    try {
      await updateMyProfile({
        age,
        gender,
        weight_kg: weightKg,
        height_cm: heightCm,
      });
      setMessage('Profile updated in MongoDB.');
    } catch (e) {
      setError(getApiErrorMessage(e));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <Header />
      <main className="container mx-auto px-4 py-8 max-w-lg">
        <Link to="/" className="text-sm text-blue-600 hover:underline">
          ← Back to home
        </Link>
        <h1 className="text-2xl font-bold text-slate-900 mt-4 mb-2">Settings</h1>
        <p className="text-slate-600 text-sm mb-6">
          Age, gender, weight, and height are used for predictions and stored in your account.
        </p>

        {loading ? (
          <p className="text-slate-500">Loading…</p>
        ) : (
          <form onSubmit={handleSave} className="bg-white p-6 rounded-xl border border-slate-200 space-y-4">
            {message && <p className="text-sm text-emerald-700">{message}</p>}
            {error && <p className="text-sm text-red-700">{error}</p>}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Age</label>
              <input
                type="number"
                min={1}
                max={120}
                value={age}
                onChange={(e) => setAge(Number(e.target.value))}
                className="w-full px-4 py-2 rounded-lg border border-slate-300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Gender</label>
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value as Gender)}
                className="w-full px-4 py-2 rounded-lg border border-slate-300"
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Weight (kg)</label>
              <input
                type="number"
                step="0.1"
                min={1}
                value={weightKg}
                onChange={(e) => setWeightKg(Number(e.target.value))}
                className="w-full px-4 py-2 rounded-lg border border-slate-300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Height (cm)</label>
              <input
                type="number"
                step={0.1}
                min={1}
                value={heightCm}
                onChange={(e) => setHeightCm(Number(e.target.value))}
                className="w-full px-4 py-2 rounded-lg border border-slate-300"
              />
            </div>
            <button
              type="submit"
              disabled={saving}
              className="w-full py-2 bg-blue-600 text-white font-semibold rounded-lg disabled:opacity-60"
            >
              {saving ? 'Saving…' : 'Save changes'}
            </button>
          </form>
        )}
      </main>
    </div>
  );
};

export default SettingsPage;
