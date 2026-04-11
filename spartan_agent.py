import os
import logging
from uagents import Agent, Context
from uagents_core.utils.registration import (
    register_chat_agent,
    RegistrationRequestCredentials,
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔱 Initialize the Agent
# In 0.24.0+, providing a port automatically starts the internal REST server
spartan_agent = Agent(
    name=os.getenv("AGENT_NAME", "spartan_bio_validate"),
    seed=os.getenv("AGENT_SEED_PHRASE"),
    port=8000,
    endpoint=f"{os.getenv('RAILWAY_URL')}/endpoint"
)

@spartan_agent.on_event("startup")
async def on_startup(ctx: Context):
    logger.info(f"🔱 SPARTAN IDENTITY: {spartan_agent.address}")
    
    # 🔱 The Master Handshake with Agentverse
    try:
        register_chat_agent(
            "SPOPS_PROXY",
            f"{os.getenv('RAILWAY_URL')}/endpoint",
            active=True,
            credentials=RegistrationRequestCredentials(
                agentverse_api_key=os.environ["AGENTVERSE_KEY"],
                agent_seed_phrase=os.environ["AGENT_SEED_PHRASE"],        
            ),
        )
        logger.info("✅ PROXY HANDSHAKE SUCCESSFUL")
    except Exception as e:
        logger.error(f"❌ PROXY REGISTRATION FAILED: {e}")

@spartan_agent.on_interval(period=60.0)
async def heartbeat(ctx: Context):
    logger.info("💓 [SPOPS HEARTBEAT] Proxy Mesh Nominal")

if __name__ == "__main__":
    # 🔱 .run() starts the agent and the internal server on the port specified above
    spartan_agent.run()
