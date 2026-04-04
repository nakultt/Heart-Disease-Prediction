import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import { fetchMyProfile, getApiErrorMessage, updateMyProfile } from '../services/api';

const DemographicsPage: React.FC = () => {
  const [smoking, setSmoking] = useState<string>('never');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const p = await fetchMyProfile();
        if (!cancelled) setSmoking(p.smoking);
      } catch {
        if (!cancelled) setError('Could not load profile.');
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
        smoking: smoking as 'never' | 'former' | 'current',
      });
      setMessage('Saved to your account.');
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
        <h1 className="text-2xl font-bold text-slate-900 mt-4 mb-2">Patient demographics</h1>
        <p className="text-slate-600 text-sm mb-6">
          Update fields you may change often. Age and gender are in Settings.
        </p>

        {loading ? (
          <p className="text-slate-500">Loading…</p>
        ) : (
          <form onSubmit={handleSave} className="bg-white p-6 rounded-xl border border-slate-200 space-y-4">
            {message && <p className="text-sm text-emerald-700">{message}</p>}
            {error && <p className="text-sm text-red-700">{error}</p>}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Smoking</label>
              <select
                value={smoking}
                onChange={(e) => setSmoking(e.target.value)}
                className="w-full px-4 py-2 rounded-lg border border-slate-300"
              >
                <option value="never">Never</option>
                <option value="former">Former</option>
                <option value="current">Current</option>
              </select>
            </div>
            <button
              type="submit"
              disabled={saving}
              className="w-full py-2 bg-blue-600 text-white font-semibold rounded-lg disabled:opacity-60"
            >
              {saving ? 'Saving…' : 'Save'}
            </button>
          </form>
        )}
      </main>
    </div>
  );
};

export default DemographicsPage;
