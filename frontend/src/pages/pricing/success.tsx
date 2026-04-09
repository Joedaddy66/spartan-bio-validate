/**
 * Pricing Success Page
 * Shown after a successful Stripe Checkout redirect.
 */
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';

export default function PricingSuccess() {
  const { query } = useRouter();
  const client = query.client ? decodeURIComponent(String(query.client)) : null;

  return (
    <>
      <Head>
        <title>Deal Closed — Spartan Bio-Validate</title>
        <meta name="description" content="Your Spartan Bio-Validate engagement has been confirmed." />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Space+Grotesk:wght@600;700&display=swap"
          rel="stylesheet"
        />
      </Head>

      <style>{`
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
          font-family: 'Inter', sans-serif;
          background: #05070f;
          color: #e8eaf0;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .bg-glow {
          position: fixed; inset: 0; z-index: 0;
          background: radial-gradient(ellipse 60% 50% at 50% 30%, rgba(52,211,153,0.12) 0%, transparent 70%);
          pointer-events: none;
        }
        .card {
          position: relative; z-index: 1;
          max-width: 520px; width: 100%;
          margin: 24px;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(52,211,153,0.25);
          border-radius: 24px;
          padding: 56px 48px;
          text-align: center;
          backdrop-filter: blur(20px);
        }
        .icon {
          font-size: 64px;
          margin-bottom: 24px;
          display: block;
          animation: pop 0.5s cubic-bezier(.34,1.56,.64,1) both;
        }
        @keyframes pop { from { transform: scale(0.5); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        h1 {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 2rem; font-weight: 700;
          background: linear-gradient(135deg, #34d399, #6ee7b7);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          margin-bottom: 12px;
        }
        p.sub {
          font-size: 0.95rem; color: #64748b; line-height: 1.6;
          margin-bottom: 32px;
        }
        .client-badge {
          display: inline-block;
          background: rgba(52,211,153,0.1);
          border: 1px solid rgba(52,211,153,0.25);
          border-radius: 999px;
          padding: 6px 18px;
          font-size: 0.85rem; font-weight: 600;
          color: #34d399;
          margin-bottom: 32px;
        }
        .links { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
        a.btn {
          padding: 12px 28px; border-radius: 10px;
          font-size: 0.9rem; font-weight: 600;
          text-decoration: none; transition: transform 0.15s, box-shadow 0.2s;
        }
        a.btn-primary {
          background: linear-gradient(135deg, #6366f1, #818cf8);
          color: #fff;
          box-shadow: 0 4px 20px rgba(99,102,241,0.35);
        }
        a.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(99,102,241,0.5); }
        a.btn-secondary {
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.1);
          color: #94a3b8;
        }
        a.btn-secondary:hover { background: rgba(255,255,255,0.08); color: #e8eaf0; }
      `}</style>

      <div className="bg-glow" />

      <div className="card">
        <span className="icon">✅</span>
        <h1>Deal Closed.</h1>

        {client && (
          <div className="client-badge">🏢 {client}</div>
        )}

        <p className="sub">
          Your sovereign engagement is confirmed. The Spartan Bio-Validate
          engine is being provisioned. You'll receive a receipt and onboarding
          details at the email provided during checkout.
        </p>

        <div className="links">
          <Link href="/" className="btn btn-primary">← Go to Dashboard</Link>
          <Link href="/pricing/negotiate" className="btn btn-secondary">New Engagement</Link>
        </div>
      </div>
    </>
  );
}
