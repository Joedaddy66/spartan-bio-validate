from fastapi import FastAPI, Request, Header, HTTPException
from core.tasks import process_genomic_batch
from core.skyfire_bridge import skyfire
import asyncio
import os
import stripe

app = FastAPI(title="Spartan Overseer Gateway")

@app.post("/submit")
@app.post("/validate")
async def receive_genomic_payload(
    request: Request,
    x_skyfire_pay_token: str = Header(None),
    x_skyfire_agent_id: str = Header(None)
):
    # 1. Skyfire Marketplace Authentication (Revenue Loop)
    if x_skyfire_pay_token:
        print(f"🪙 Received Skyfire request from agent: {x_skyfire_agent_id}")
        # Charge the agent $0.10 as requested by user
        charge = await skyfire.verify_and_charge(x_skyfire_pay_token, amount_usd=0.10)
        if not charge["success"]:
            raise HTTPException(status_code=402, detail=f"Skyfire Payment Required: {charge['error']}")
        print(f"✅ Skyfire Revenue Collected: {charge['transaction_id']}")

    # 2. Catch the data from Agentverse, Cloudflare, or local Proxy Agent
    try:
        data = await request.json()
    except:
        data = {}
        
    batch_id = data.get("batch_id", f"BATCH_{int(asyncio.get_event_loop().time())}")
    sequences = data.get("sequences", [])
    
    if not sequences:
        return {"success": False, "error": "No sequences found in payload", "batch_id": batch_id}

    # 3. Hand it off to the Celery Muscle (Non-blocking)
    task = process_genomic_batch.delay(batch_id, sequences)
    
    return {
        "success": True, 
        "batch_id": batch_id, 
        "job_id": task.id, 
        "status": "QUEUED",
        "timestamp": asyncio.get_event_loop().time(),
        "payment": "Skyfire" if x_skyfire_pay_token else "Direct/Stripe"
    }

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Handle Stripe Webhooks to bridge 'Pay' to 'Validation'
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # Extract metadata from Phase 1 checkout
        client_name = session.get("metadata", {}).get("clientName", "Anonymous")
        record_count = session.get("metadata", {}).get("recordCount")
        
        print(f"💰 Stripe Payment Confirmed for {client_name} ({record_count} records)")
        # Here we could trigger a specific batch if the user uploaded it previously
        
    return {"status": "success"}

# Health check route
@app.get("/")
def health_check():
    return {"status": "🔱 SPARTAN OVERSEER: UNIFIED GATEWAY ACTIVE", "skyfire": "READY"}
