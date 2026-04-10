import os
import asyncio
import uuid
from uagents import Agent, Context, Bureau
from loguru import logger
from dotenv import load_dotenv

# --- 1. THE LAZARUS COMBER (REVERSAL DISTANCE LOGIC) ---
def get_lazarus_signature(sequence):
    """
    Combs a sequence to find the structural 'flip' count.
    This is the core biometric of the Lazarus Protocol.
    """
    flips = 0
    arr = list(sequence)
    for i in range(len(arr)):
        target = i + 1
        if arr[i] != target and target in arr:
            idx = arr.index(target)
            arr[i:idx+1] = reversed(arr[i:idx+1])
            flips += 1
    return flips

# --- 2. ENVIRONMENT & IDENTITY ---
load_dotenv()
# Railway automatically assigns a replica index; we use it to link the 5 workers
WORKER_INDEX = os.getenv("RAILWAY_REPLICA_NUMBER", "0")
AGENT_SEED = os.getenv("AGENT_SEED", "spartan01_2026_vault")

# All workers share the same seed (Wallet) but have unique sub-names
spartan_worker = Agent(
    name=f"spartan-bio-worker-{WORKER_INDEX}",
    seed=AGENT_SEED,
    port=8000 + int(WORKER_INDEX),
    endpoint=[f"http://localhost:{8000 + int(WORKER_INDEX)}/submit"]
)

# --- 3. THE AUTONOMOUS COMBING LOOP ---
@spartan_worker.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🔱 Worker {WORKER_INDEX} Online | Address: {spartan_worker.address}")

@spartan_worker.on_interval(period=15.0)
async def comb_sequences(ctx: Context):
    """
    Acquires sequences and links them via a severity-weighted sort.
    """
    ctx.logger.info(f"Worker {WORKER_INDEX}: Combing 1,001 Sequence Mesh...")
    
    # MOCK: In production, this pulls from your 1,001 acquired sequences
    # Sequence [1, 3, 2, 4] represents a 'flipped' gene block
    mock_batch = [
        {"id": "SEQ-001", "data": [1, 2, 3, 4]}, # Stable
        {"id": "SEQ-742", "data": [1, 4, 3, 2, 6, 5]} # Lazarus Signature (Drift)
    ]

    for item in mock_batch:
        severity = get_lazarus_signature(item['data'])
        
        if severity >= 2:
            ctx.logger.info(f"🔱 LAZARUS HIT | ID: {item['id']} | Severity: {severity}")
            
            # THE LINKER DATA: This is what you push to your DB for Vercel
            payload = {
                "worker_id": WORKER_INDEX,
                "sequence_id": item['id'],
                "severity": severity,
                "timestamp": str(asyncio.get_event_loop().time()),
                "coords": [1.5, 0, severity * 0.5] # Z-Axis reflects drift intensity
            }
            
            # TODO: push_to_db(payload) - This links the 5 workers in your DB
            ctx.logger.info(f"Sequence {item['id']} Sorted & Prepped for Telemetry.")

# --- 4. THE IMMORTAL BOOTLOADER ---
async def run_mesh():
    bureau = Bureau(port=8000 + int(WORKER_INDEX))
    bureau.add(spartan_worker)
    await bureau.run_async()

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(run_mesh())
        except Exception as e:
            logger.error(f"Restarting Worker {WORKER_INDEX} due to: {e}")
            continue
        except KeyboardInterrupt:
            break
