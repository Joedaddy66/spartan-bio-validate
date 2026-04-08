/**
 * Dynamic Checkout API
 * Generates a Stripe Checkout Session for sovereign broker pricing.
 * Accepts a pre-calculated total from dynamic-calculate and creates
 * a one-time payment session scoped to the negotiated engagement.
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
    const {
      clientName,
      recordCount,
      requiresLazarus,
      requiresFIPS,
      finalPrice, // amount in cents from dynamic-calculate
      description,
    } = req.body;

    if (!finalPrice || finalPrice <= 0) {
      return res.status(400).json({ error: 'finalPrice must be a positive number in cents' });
    }

    const engagementLabel = [
      `${recordCount?.toLocaleString() ?? '?'} Sequences`,
      requiresLazarus ? '+ Lazarus Protocol' : '',
      requiresFIPS ? '+ FIPS-140-2 L3' : '',
    ]
      .filter(Boolean)
      .join(' ');

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items: [
        {
          price_data: {
            currency: 'usd',
            unit_amount: finalPrice,
            product_data: {
              name: `Spartan Bio-Validate — Sovereign Engagement`,
              description: description ?? engagementLabel,
              metadata: {
                client: clientName ?? 'Anonymous',
                recordCount: String(recordCount ?? 0),
                lazarus: String(!!requiresLazarus),
                fips: String(!!requiresFIPS),
              },
            },
          },
          quantity: 1,
        },
      ],
      success_url: `${process.env.NEXT_PUBLIC_BASE_URL}/pricing/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXT_PUBLIC_BASE_URL}/pricing/negotiate`,
      metadata: {
        client: clientName ?? 'Anonymous',
        recordCount: String(recordCount ?? 0),
        lazarus: String(!!requiresLazarus),
        fips: String(!!requiresFIPS),
        generatedAt: new Date().toISOString(),
      },
    });

    return res.status(200).json({ url: session.url, sessionId: session.id });
  } catch (error: any) {
    console.error('[dynamic-checkout] Error:', error);
    return res.status(500).json({ error: error.message ?? 'Internal server error' });
  }
}
