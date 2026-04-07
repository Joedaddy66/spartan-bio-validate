const express = require('express');
const router = express.Router();
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

router.post('/dynamic-checkout', async (req, res) => {
  const { clientName, recordCount, requiresLazarus, requiresFIPS } = req.body;

  let unitCostCents = 10; 
  if (requiresLazarus) unitCostCents *= 3; 
  
  let totalAmountCents = recordCount * unitCostCents;
  if (requiresFIPS) totalAmountCents += 5000000; 

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card', 'us_bank_account'],
      line_items: [
        {
          price_data: {
            currency: 'usd',
            product_data: {
              name: `Spartan Bio-Validate: Custom Integration for ${clientName}`,
              description: `${recordCount.toLocaleString()} sequences mapped to 4^12 coordinates.`,
            },
            unit_amount: totalAmountCents,
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: 'https://spartan-bio-validate.vercel.app/dashboard?deal=closed',
      cancel_url: 'https://spartan-bio-validate.vercel.app/negotiation',
      client_reference_id: "SPARTAN_OMEGA_7"
    });

    res.json({ url: session.url, finalPrice: totalAmountCents / 100 });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
