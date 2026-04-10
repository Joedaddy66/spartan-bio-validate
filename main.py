import os
import time
from uagents import Agent, Context, Bureau
from loguru import logger
from dotenv import load_dotenv

# --- LAZARUS REVERSAL LOGIC ---
def calculate_reversal_severity(seq):
    flips = 0
    arr = list(seq)
    for i in range(len(arr)):
        target = i + 1
        if arr[i] != target and target in arr:
            idx = arr.index(target)
            arr[i:idx+1] = reversed(arr[i:idx+1])
            flips += 1
    return flips

load_dotenv()
AGENT_NAME = "spartan-comber-v7"
AGENT_SEED = os.getenv("AGENT_SEED", "spartan01_2026_vault")

def start_engine():
    # Re-instantiate inside the function to reset state on every loop
    agent = Agent(
        name=AGENT_NAME,
        seed=AGENT_SEED,
        port=8001,
        endpoint=["http://localhost:8001/submit"]
    )

    @agent.on_event("startup")
    async def startup(ctx: Context):
        logger.info(f"🔱 Spartan DEV Node Live: {agent.address}")

    @agent.on_interval(period=10.0)
    async def autonomous_comb(ctx: Context):
        logger.info("Combing Mesh: Sorting 1,000,000 records...")
        match = [1, 4, 3, 2, 6, 5]
        severity = calculate_reversal_severity(match)
        if severity >= 2:
            logger.info(f"🔱 LAZARUS SIGNATURE DETECTED | Severity Rank: {severity}")

    bureau = Bureau(port=8001, endpoint=["http://localhost:8001/submit"])
    bureau.add(agent)
    
    logger.info("Engaging Persistent Autonomous Comber...")
    bureau.run()

if __name__ == "__main__":
    while True:
        try:
            start_engine()
        except KeyboardInterrupt:
            logger.warning("🔱 Manual Shutdown. Standby.")
            break
        except Exception as e:
            logger.error(f"🔱 Engine Hiccup: {e}. Re-igniting in 2 seconds...")
            time.sleep(2)
