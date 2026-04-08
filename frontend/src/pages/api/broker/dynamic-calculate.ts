/**
 * Dynamic Pricing Calculator API
 * Calculates custom pricing based on data weight and requirements.
 * Lazarus Protocol: 3x multiplier on per-sequence base cost.
 * FIPS-140-2 L3: flat $50,000 premium for enterprise compliance.
 */
import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { clientName, recordCount, requiresLazarus, requiresFIPS } = req.body;

    if (!recordCount || recordCount <= 0) {
      return res.status(400).json({ error: 'recordCount must be a positive number' });
    }

    // Base pricing: $0.10 per sequence = 10 cents
    let unitCostCents = 10;

    // Lazarus Protocol: 3x multiplier for advanced compute
    if (requiresLazarus) {
      unitCostCents = unitCostCents * 3; // $0.30/sequence
    }

    // FIPS Premium: $50,000 flat fee
    const fipsPremiumCents = requiresFIPS ? 5_000_000 : 0; // $50,000 in cents

    // Calculate totals
    const baseCostCents = recordCount * unitCostCents;
    const lazarusPremiumCents = requiresLazarus ? recordCount * 20 : 0; // the 2x delta over base
    const totalAmountCents = baseCostCents + fipsPremiumCents;

    return res.status(200).json({
      clientName: clientName || 'Anonymous',
      recordCount,
      unitCostCents,
      baseCostDollars: baseCostCents / 100,
      lazarusPremiumDollars: lazarusPremiumCents / 100,
      fipsPremiumDollars: fipsPremiumCents / 100,
      finalPrice: totalAmountCents,        // in cents (for Stripe)
      finalPriceDollars: totalAmountCents / 100,
      currency: 'USD',
      breakdown: {
        base: `${recordCount.toLocaleString()} sequences × $${(unitCostCents / 100).toFixed(2)}`,
        lazarus: requiresLazarus ? '3× multiplier applied' : null,
        fips: requiresFIPS ? '$50,000 FIPS-140-2 L3 compliance fee' : null,
      },
      calculatedAt: new Date().toISOString(),
    });
  } catch (error: any) {
    console.error('[dynamic-calculate] Error:', error);
    return res.status(500).json({ error: error.message ?? 'Internal server error' });
  }
}
