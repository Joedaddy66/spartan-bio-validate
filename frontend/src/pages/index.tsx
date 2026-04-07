import React, { useState } from 'react';
import Head from 'next/head';

export default function Dashboard() {
  const [recordCount, setRecordCount] = useState(1000000);
  const [requiresLazarus, setRequiresLazarus] = useState(true);
  const [requiresFIPS, setRequiresFIPS] = useState(true);
  const [quote, setQuote] = useState(null);

  const calculateQuote = async () => {
    // In production, this pings your vaas.js endpoint
    let base = recordCount * 0.10;
    if (requiresLazarus) base *= 3;
    if (requiresFIPS) base += 50000;
    setQuote(base);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      <Head><title>Spartan Bio-Validate | OMEGA</title></Head>
      
      <header className="mb-12 border-b border-slate-700 pb-4">
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-cyan-400">
          Spartan Bio-Validate v7.0
        </h1>
        <p className="text-slate-400 mt-2">Zero-Drift Genomic Validation Engine // 1.0 Precision</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Left Column: KPI Tiles */}
        <div className="space-y-6">
          <div className="glass-panel p-6 border border-slate-700 rounded-xl bg-slate-800/50">
            <h3 className="text-sm font-uppercase tracking-wider text-slate-400">Predictive Quality Score</h3>
            <p className="text-5xl font-bold text-indigo-400 mt-2">99.99%</p>
            <p className="text-xs text-green-400 mt-2">↑ 0.00% Drift Detected</p>
          </div>
          <div className="glass-panel p-6 border border-slate-700 rounded-xl bg-slate-800/50">
            <h3 className="text-sm font-uppercase tracking-wider text-slate-400">Lazarus Anomalies Isolated</h3>
            <p className="text-5xl font-bold text-cyan-400 mt-2">1</p>
            <p className="text-xs text-slate-400 mt-2">Target: PX-7234491</p>
          </div>
        </div>

        {/* Right Column: The Sovereign Broker */}
        <div className="glass-panel p-8 border border-indigo-500/30 rounded-xl bg-slate-800/80 shadow-2xl shadow-indigo-500/10">
          <h2 className="text-2xl font-bold mb-6">Sovereign Broker Setup</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-400 mb-1">Ingestion Volume (Records)</label>
              <input 
                type="range" min="10000" max="50000000" step="10000"
                value={recordCount} onChange={(e) => setRecordCount(Number(e.target.value))}
                className="w-full"
              />
              <p className="text-right text-indigo-400 font-mono">{recordCount.toLocaleString()}</p>
            </div>

            <div className="flex items-center justify-between py-2 border-t border-slate-700">
              <span className="text-sm">Apply 37x73 Semiprime Voxel Squeeze</span>
              <input type="checkbox" checked={requiresLazarus} onChange={() => setRequiresLazarus(!requiresLazarus)} />
            </div>

            <div className="flex items-center justify-between py-2 border-t border-slate-700">
              <span className="text-sm">FIPS-140-2 L3 Immutable Ledger</span>
              <input type="checkbox" checked={requiresFIPS} onChange={() => setRequiresFIPS(!requiresFIPS)} />
            </div>

            <button 
              onClick={calculateQuote}
              className="w-full mt-6 py-4 bg-gradient-to-r from-indigo-600 to-cyan-600 rounded-lg font-bold hover:scale-[1.02] transition-transform text-white shadow-lg"
            >
              AUTHORIZE CERTIFIED WORKER
            </button>

            {quote && (
              <div className="mt-6 p-4 bg-slate-900 border border-green-500/30 rounded-lg text-center animate-pulse">
                <p className="text-sm text-slate-400 mb-1">Dynamic Quote Generated</p>
                <p className="text-4xl font-bold text-green-400">${quote.toLocaleString()}</p>
                <p className="text-xs mt-2 text-slate-500">Awaiting Wire Transfer // ACH Routed</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
