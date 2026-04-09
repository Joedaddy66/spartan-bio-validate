/**
 * Dynamic Checkout Generator API — Sovereign Broker v1
 * Generates a custom Stripe Checkout session in real-time per deal.
 * Uses price_data (not a stored Price ID) so every session is sovereign.
 * Pricing is computed server-side — do NOT trust a finalPrice from the client.
 */
import { NextApiRequest, NextApiResponse } from 'next';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { clientName, recordCount, requiresLazarus, requiresFIPS } = req.body;

    if (!clientName) {
      return res.status(400).json({ error: 'clientName is required' });
    }
    if (!recordCount || recordCount <= 0) {
      return res.status(400).json({ error: 'recordCount must be a positive number' });
    }

    // ── Pricing engine (authoritative — matches dynamic-calculate) ──────────
    let unitCostCents = 10; // $0.10 / sequence base
    if (requiresLazarus) unitCostCents *= 3; // → $0.30 with Lazarus 3×

    const fipsPremiumCents = requiresFIPS ? 5_000_000 : 0; // $50,000 flat
    const totalAmountCents = recordCount * unitCostCents + fipsPremiumCents;

    if (totalAmountCents < 50) {
      return res.status(400).json({ error: 'Calculated amount is below Stripe minimum ($0.50). Increase record count.' });
    }

    // ── Human-readable deal description ────────────────────────────────────
    const featureLines: string[] = [
      `${Number(recordCount).toLocaleString()} sequences → 4¹² coordinate mapping`,
    ];
    if (requiresLazarus) featureLines.push('Lazarus Protocol (1-in-847M singularity detection via 37×73=2701 semiprime anchor)');
    if (requiresFIPS)    featureLines.push('FIPS-140-2 L3 Immutable Ledger (FDA 483 remediation, cryptographic audit trails)');
    const description = featureLines.join(' | ');

    // ── Base URL resolution ─────────────────────────────────────────────────
    const baseUrl =
      process.env.NEXT_PUBLIC_BASE_URL ??
      (process.env.NEXT_PUBLIC_VERCEL_URL ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}` : null) ??
      process.env.NEXT_PUBLIC_RAILWAY_API_URL ??
      'http://localhost:3000';

    // ── Stripe Checkout session ─────────────────────────────────────────────
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card', 'us_bank_account'],
      line_items: [
        {
          price_data: {
            currency: 'usd',
            product_data: {
              name: `Spartan Bio-Validate — Custom Integration for ${clientName}`,
              description,
              metadata: {
                clientName,
                recordCount:     String(recordCount),
                requiresLazarus: String(!!requiresLazarus),
                requiresFIPS:    String(!!requiresFIPS),
              },
            },
            unit_amount: totalAmountCents,
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `${baseUrl}/pricing/success?session_id={CHECKOUT_SESSION_ID}&client=${encodeURIComponent(clientName)}`,
      cancel_url:  `${baseUrl}/pricing/negotiate`,
      metadata: {
        client_name:     clientName,
        record_count:    String(recordCount),
        pricing_model:   'dynamic_sovereign_broker_v1',
        lazarus_enabled: String(!!requiresLazarus),
        fips_enabled:    String(!!requiresFIPS),
        timestamp:       new Date().toISOString(),
      },
    });

    return res.status(200).json({
      success:      true,
      url:          session.url,
      sessionId:    session.id,
      finalPrice:   totalAmountCents / 100,
      currency:     'USD',
      calculatedAt: new Date().toISOString(),
    });
  } catch (error: any) {
    console.error('[dynamic-checkout] Error:', error);
    return res.status(500).json({ error: error.message ?? 'Internal server error' });
  }
}
