from fastapi import FastAPI, Request
from core.tasks import process_genomic_batch

app = FastAPI(title="Spartan Overseer Gateway")

@app.post("/submit")
async def receive_genomic_payload(request: Request):
    # 1. Catch the data from Agentverse or Cloudflare
    data = await request.json()
    batch_id = data.get("batch_id", "UNKNOWN_BATCH")
    sequences = data.get("sequences", [])
    
    # 2. Hand it off to the Celery Muscle (Non-blocking)
    # The .delay() means "put this in Redis and let the workers handle it"
    task = process_genomic_batch.delay(batch_id, sequences)
    
    # 3. Wait for the result and return it to Agentverse
    result = task.get(timeout=30) 
    
    return result

# Health check route
@app.get("/")
def health_check():
    return {"status": "🔱 SPARTAN OVERSEER: MACRO-MESH ACTIVE"}
