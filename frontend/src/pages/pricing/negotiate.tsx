import { useState, useEffect, useCallback } from 'react';
import Head from 'next/head';

interface PriceBreakdown {
  clientName: string;
  recordCount: number;
  unitCostCents: number;
  baseCostDollars: number;
  lazarusPremiumDollars: number;
  fipsPremiumDollars: number;
  finalPrice: number;
  finalPriceDollars: number;
  currency: string;
  breakdown: {
    base: string;
    lazarus: string | null;
    fips: string | null;
  };
  calculatedAt: string;
}

const fmt = (n: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);

export default function NegotiatePage() {
  const [clientName, setClientName] = useState('');
  const [recordCount, setRecordCount] = useState(100_000);
  const [requiresLazarus, setRequiresLazarus] = useState(false);
  const [requiresFIPS, setRequiresFIPS] = useState(false);
  const [quote, setQuote] = useState<PriceBreakdown | null>(null);
  const [loading, setLoading] = useState(false);
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const calculate = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/broker/dynamic-calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clientName, recordCount, requiresLazarus, requiresFIPS }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      setQuote(data);
    } catch (e: any) {
      setError(e.message ?? 'Calculation failed');
    } finally {
      setLoading(false);
    }
  }, [clientName, recordCount, requiresLazarus, requiresFIPS]);

  useEffect(() => {
    const t = setTimeout(() => { calculate(); }, 400);
    return () => clearTimeout(t);
  }, [calculate]);

  const handleCheckout = async () => {
    if (!quote) return;
    setCheckoutLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/broker/dynamic-checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          clientName,
          recordCount,
          requiresLazarus,
          requiresFIPS,
          finalPrice: quote.finalPrice,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      window.location.href = data.url;
    } catch (e: any) {
      setError(e.message ?? 'Checkout failed');
    } finally {
      setCheckoutLoading(false);
    }
  };

  const sliderMax = 5_000_000;

  return (
    <>
      <Head>
        <title>Sovereign Broker — Negotiate Your Engagement | Spartan Bio-Validate</title>
        <meta
          name="description"
          content="Configure your data validation engagement with real-time pricing. Choose sequence volume, Lazarus Protocol, and FIPS-140-2 L3 compliance for a custom quote."
        />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </Head>

      <style jsx global>{`
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html { scroll-behavior: smooth; }
        body {
          font-family: 'Inter', system-ui, sans-serif;
          background: #05070f;
          color: #e8eaf0;
          min-height: 100vh;
        }

        /* ── grid glow bg ── */
        .bg-grid {
          position: fixed; inset: 0; z-index: 0;
          background-image:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,102,241,0.25) 0%, transparent 70%),
            linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
          background-size: auto, 48px 48px, 48px 48px;
          pointer-events: none;
        }

        .page-wrap {
          position: relative; z-index: 1;
          max-width: 880px; margin: 0 auto;
          padding: 64px 24px 96px;
        }

        /* ── header ── */
        .eyebrow {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 11px; font-weight: 600; letter-spacing: 0.18em;
          text-transform: uppercase;
          color: #818cf8;
          margin-bottom: 14px;
          display: flex; align-items: center; gap: 8px;
        }
        .eyebrow::before {
          content: ''; display: block;
          width: 20px; height: 2px;
          background: linear-gradient(90deg, #6366f1, #818cf8);
          border-radius: 2px;
        }
        h1 {
          font-family: 'Space Grotesk', sans-serif;
          font-size: clamp(32px, 5vw, 52px);
          font-weight: 700;
          line-height: 1.1;
          background: linear-gradient(135deg, #e8eaf0 30%, #818cf8);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          background-clip: text;
          margin-bottom: 16px;
        }
        .subtitle {
          font-size: 16px; color: #94a3b8; line-height: 1.6;
          max-width: 560px; margin-bottom: 48px;
        }

        /* ── card ── */
        .card {
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 20px;
          padding: 36px;
          backdrop-filter: blur(12px);
          margin-bottom: 20px;
          transition: border-color 0.3s;
        }
        .card:hover { border-color: rgba(99,102,241,0.25); }

        .card-label {
          font-size: 11px; font-weight: 600; letter-spacing: 0.12em;
          text-transform: uppercase; color: #64748b;
          margin-bottom: 20px;
        }

        /* ── name input ── */
        .field { margin-bottom: 28px; }
        .field label {
          display: block; font-size: 13px; font-weight: 500; color: #94a3b8;
          margin-bottom: 8px;
        }
        .field input {
          width: 100%; padding: 12px 16px;
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 10px; color: #e8eaf0; font-size: 15px;
          font-family: 'Inter', sans-serif;
          outline: none; transition: border-color 0.2s, box-shadow 0.2s;
        }
        .field input:focus {
          border-color: #6366f1;
          box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
        }

        /* ── slider ── */
        .slider-wrap { margin-bottom: 8px; }
        .slider-row {
          display: flex; justify-content: space-between; align-items: baseline;
          margin-bottom: 12px;
        }
        .slider-title { font-size: 15px; font-weight: 500; }
        .slider-value {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 22px; font-weight: 700; color: #818cf8;
        }
        input[type="range"] {
          -webkit-appearance: none; appearance: none;
          width: 100%; height: 6px;
          background: rgba(255,255,255,0.08);
          border-radius: 6px; cursor: pointer; outline: none;
        }
        input[type="range"]::-webkit-slider-thumb {
          -webkit-appearance: none; appearance: none;
          width: 22px; height: 22px; border-radius: 50%;
          background: linear-gradient(135deg, #6366f1, #818cf8);
          box-shadow: 0 0 12px rgba(99,102,241,0.6);
          cursor: pointer; transition: transform 0.15s;
        }
        input[type="range"]::-webkit-slider-thumb:hover { transform: scale(1.15); }

        /* ── toggles ── */
        .toggles { display: grid; gap: 14px; }
        .toggle-row {
          display: flex; align-items: center; justify-content: space-between;
          padding: 16px 20px;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 12px; cursor: pointer;
          transition: background 0.2s, border-color 0.2s;
          user-select: none;
        }
        .toggle-row:hover { background: rgba(99,102,241,0.07); border-color: rgba(99,102,241,0.2); }
        .toggle-row.active { background: rgba(99,102,241,0.1); border-color: rgba(99,102,241,0.35); }

        .toggle-info { flex: 1; padding-right: 16px; }
        .toggle-name { font-size: 14px; font-weight: 600; margin-bottom: 2px; }
        .toggle-desc { font-size: 12px; color: #64748b; }

        .toggle-pill {
          width: 46px; height: 26px; border-radius: 13px;
          background: rgba(255,255,255,0.1);
          position: relative; transition: background 0.25s;
          flex-shrink: 0;
        }
        .toggle-pill.on { background: linear-gradient(90deg, #6366f1, #818cf8); }
        .toggle-pill::after {
          content: '';
          position: absolute; top: 3px; left: 3px;
          width: 20px; height: 20px; border-radius: 50%;
          background: #fff;
          box-shadow: 0 1px 4px rgba(0,0,0,0.4);
          transition: transform 0.25s cubic-bezier(.34,1.56,.64,1);
        }
        .toggle-pill.on::after { transform: translateX(20px); }

        /* ── quote panel ── */
        .quote-panel {
          background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(129,140,248,0.04) 100%);
          border: 1px solid rgba(99,102,241,0.25);
          border-radius: 20px; padding: 36px;
          position: sticky; top: 24px;
        }
        .quote-label {
          font-size: 11px; font-weight: 600; letter-spacing: 0.12em;
          text-transform: uppercase; color: #818cf8; margin-bottom: 24px;
        }
        .quote-total {
          font-family: 'Space Grotesk', sans-serif;
          font-size: clamp(36px, 5vw, 52px); font-weight: 700;
          background: linear-gradient(135deg, #c7d2fe, #818cf8);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          background-clip: text;
          margin-bottom: 24px;
          min-height: 60px; display: flex; align-items: center;
        }
        .quote-lines { margin-bottom: 28px; }
        .quote-line {
          display: flex; justify-content: space-between; align-items: center;
          padding: 10px 0;
          border-bottom: 1px solid rgba(255,255,255,0.05);
          font-size: 13px;
        }
        .quote-line:last-child { border-bottom: none; }
        .q-key { color: #64748b; }
        .q-val { font-weight: 600; color: #e8eaf0; }
        .q-val.accent { color: #818cf8; }

        .badge {
          display: inline-block;
          padding: 3px 10px; border-radius: 99px;
          font-size: 11px; font-weight: 600; letter-spacing: 0.06em;
          margin-left: 6px;
        }
        .badge-lazarus {
          background: rgba(244,63,94,0.15); color: #fb7185;
          border: 1px solid rgba(244,63,94,0.25);
        }
        .badge-fips {
          background: rgba(16,185,129,0.12); color: #34d399;
          border: 1px solid rgba(16,185,129,0.2);
        }

        /* ── CTA button ── */
        .btn-checkout {
          width: 100%; padding: 16px;
          background: linear-gradient(135deg, #6366f1, #818cf8);
          border: none; border-radius: 12px;
          font-size: 15px; font-weight: 700;
          color: #fff; cursor: pointer;
          position: relative; overflow: hidden;
          transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
          box-shadow: 0 8px 24px rgba(99,102,241,0.35);
          font-family: 'Space Grotesk', sans-serif;
          letter-spacing: 0.03em;
        }
        .btn-checkout:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 12px 32px rgba(99,102,241,0.5);
        }
        .btn-checkout:active:not(:disabled) { transform: translateY(0); }
        .btn-checkout:disabled { opacity: 0.55; cursor: not-allowed; }

        /* ── layout ── */
        .two-col {
          display: grid;
          grid-template-columns: 1fr 340px;
          gap: 24px;
          align-items: start;
        }
        @media (max-width: 720px) {
          .two-col { grid-template-columns: 1fr; }
          .quote-panel { position: static; }
        }

        /* ── error ── */
        .error-box {
          background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.25);
          border-radius: 10px; padding: 12px 16px;
          color: #fca5a5; font-size: 13px; margin-top: 12px;
        }

        /* ── loading pulse ── */
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
        .pulsing { animation: pulse 1.2s infinite; }
      `}</style>

      <div className="bg-grid" />

      <div className="page-wrap">
        <p className="eyebrow">Sovereign Broker</p>
        <h1>Negotiate Your Engagement</h1>
        <p className="subtitle">
          Configure your data-validation workload below. Pricing is computed live — every parameter
          adjusts your quote in real time. Commit when you're ready to deploy.
        </p>

        <div className="two-col">
          {/* ── Left: controls ── */}
          <div>
            <div className="card">
              <p className="card-label">Client Identity</p>
              <div className="field">
                <label htmlFor="client-name">Organisation / Entity Name</label>
                <input
                  id="client-name"
                  type="text"
                  placeholder="e.g. Apex Genomics LLC"
                  value={clientName}
                  onChange={(e) => setClientName(e.target.value)}
                />
              </div>

              <p className="card-label">Data Weight</p>
              <div className="slider-wrap">
                <div className="slider-row">
                  <span className="slider-title">Sequence Volume</span>
                  <span className="slider-value">{recordCount.toLocaleString()}</span>
                </div>
                <input
                  id="record-count-slider"
                  type="range"
                  min={1000}
                  max={sliderMax}
                  step={1000}
                  value={recordCount}
                  onChange={(e) => setRecordCount(Number(e.target.value))}
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6, fontSize: 11, color: '#475569' }}>
                  <span>1K</span><span>5M</span>
                </div>
              </div>
            </div>

            <div className="card">
              <p className="card-label">Protocol Add-Ons</p>
              <div className="toggles">
                {/* Lazarus toggle */}
                <div
                  id="toggle-lazarus"
                  className={`toggle-row${requiresLazarus ? ' active' : ''}`}
                  role="switch"
                  aria-checked={requiresLazarus}
                  tabIndex={0}
                  onClick={() => setRequiresLazarus((v) => !v)}
                  onKeyDown={(e) => e.key === 'Enter' && setRequiresLazarus((v) => !v)}
                >
                  <div className="toggle-info">
                    <p className="toggle-name">
                      Lazarus Protocol
                      <span className="badge badge-lazarus">3× compute</span>
                    </p>
                    <p className="toggle-desc">Advanced resurrection compute — triples per-sequence cost</p>
                  </div>
                  <div className={`toggle-pill${requiresLazarus ? ' on' : ''}`} />
                </div>

                {/* FIPS toggle */}
                <div
                  id="toggle-fips"
                  className={`toggle-row${requiresFIPS ? ' active' : ''}`}
                  role="switch"
                  aria-checked={requiresFIPS}
                  tabIndex={0}
                  onClick={() => setRequiresFIPS((v) => !v)}
                  onKeyDown={(e) => e.key === 'Enter' && setRequiresFIPS((v) => !v)}
                >
                  <div className="toggle-info">
                    <p className="toggle-name">
                      FIPS-140-2 L3
                      <span className="badge badge-fips">+$50K flat</span>
                    </p>
                    <p className="toggle-desc">Federal compliance — cryptographic module certification</p>
                  </div>
                  <div className={`toggle-pill${requiresFIPS ? ' on' : ''}`} />
                </div>
              </div>
            </div>
          </div>

          {/* ── Right: live quote ── */}
          <div className="quote-panel">
            <p className="quote-label">Live Quote</p>

            <div className={`quote-total${loading ? ' pulsing' : ''}`}>
              {quote ? fmt(quote.finalPriceDollars) : '—'}
            </div>

            {quote && (
              <div className="quote-lines">
                <div className="quote-line">
                  <span className="q-key">Base cost</span>
                  <span className="q-val">{fmt(quote.baseCostDollars)}</span>
                </div>
                {quote.lazarusPremiumDollars > 0 && (
                  <div className="quote-line">
                    <span className="q-key">Lazarus uplift</span>
                    <span className="q-val accent">{fmt(quote.lazarusPremiumDollars)}</span>
                  </div>
                )}
                {quote.fipsPremiumDollars > 0 && (
                  <div className="quote-line">
                    <span className="q-key">FIPS-140-2 L3</span>
                    <span className="q-val accent">{fmt(quote.fipsPremiumDollars)}</span>
                  </div>
                )}
                <div className="quote-line">
                  <span className="q-key">Unit rate</span>
                  <span className="q-val">${(quote.unitCostCents / 100).toFixed(2)}/seq</span>
                </div>
                <div className="quote-line">
                  <span className="q-key">Sequences</span>
                  <span className="q-val">{quote.recordCount.toLocaleString()}</span>
                </div>
              </div>
            )}

            {error && <div className="error-box">⚠ {error}</div>}

            <button
              id="btn-commit-engagement"
              className="btn-checkout"
              disabled={!quote || loading || checkoutLoading}
              onClick={handleCheckout}
            >
              {checkoutLoading ? 'Redirecting…' : 'Commit Engagement →'}
            </button>

            <p style={{ fontSize: 11, color: '#475569', textAlign: 'center', marginTop: 12 }}>
              Secured via Stripe · No data stored
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
