from fastapi import FastAPI, Request
from core.tasks import process_genomic_batch
import asyncio

app = FastAPI(title="Spartan Overseer Gateway")

@app.post("/submit")
@app.post("/validate")
async def receive_genomic_payload(request: Request):
    # 1. Catch the data from Agentverse, Cloudflare, or local Proxy Agent
    try:
        data = await request.json()
    except:
        data = {}
        
    batch_id = data.get("batch_id", f"BATCH_{int(asyncio.get_event_loop().time())}")
    sequences = data.get("sequences", [])
    
    if not sequences:
        return {"success": False, "error": "No sequences found in payload", "batch_id": batch_id}

    # 2. Hand it off to the Celery Muscle (Non-blocking)
    # We pass the list of sequences directly
    task = process_genomic_batch.delay(batch_id, sequences)
    
    # 3. Wait for result without blocking (or return job_id immediately)
    # Since we want "ASAP" validation, we'll return the job details
    return {
        "success": True, 
        "batch_id": batch_id, 
        "job_id": task.id, 
        "status": "QUEUED",
        "timestamp": asyncio.get_event_loop().time()
    }

# Health check route
@app.get("/")
def health_check():
    return {"status": "🔱 SPARTAN OVERSEER: MACRO-MESH ACTIVE"}
