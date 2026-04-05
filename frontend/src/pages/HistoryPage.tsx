import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import { fetchPredictionHistory, getApiErrorMessage, type PredictionHistoryItem } from '../services/api';

const HistoryPage: React.FC = () => {
  const [rows, setRows] = useState<PredictionHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await fetchPredictionHistory();
        if (!cancelled) setRows(data);
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

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <Header />
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <Link to="/" className="text-sm text-blue-600 hover:underline">
          ← Back to home
        </Link>
        <h1 className="text-2xl font-bold text-slate-900 mt-4 mb-2">Prediction history</h1>
        <p className="text-slate-600 text-sm mb-6">All runs you have saved while logged in.</p>

        {loading && <p className="text-slate-500">Loading…</p>}
        {error && <p className="text-red-600 text-sm">{error}</p>}
        {!loading && !error && rows.length === 0 && (
          <p className="text-slate-600">No predictions yet. Use Clinical measurements to create one.</p>
        )}
        {!loading && rows.length > 0 && (
          <div className="overflow-x-auto bg-white rounded-xl border border-slate-200">
            <table className="min-w-full text-sm">
              <thead className="bg-slate-100 text-slate-700">
                <tr>
                  <th className="text-left p-3">When</th>
                  <th className="text-left p-3">Risk</th>
                  <th className="text-right p-3">Probability</th>
                  <th className="text-left p-3">Label</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.id} className="border-t border-slate-100">
                    <td className="p-3 whitespace-nowrap">
                      {r.created_at ? new Date(r.created_at).toLocaleString() : '—'}
                    </td>
                    <td className="p-3">{r.risk_level}</td>
                    <td className="p-3 text-right">{Math.round(r.probability * 100)}%</td>
                    <td className="p-3">{r.prediction === 1 ? 'Heart disease' : 'Healthy'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
};

export default HistoryPage;
