import os
import logging
from uagents import Agent, Context, AgentServer
from uagents_core.utils.registration import (
    register_chat_agent,
    RegistrationRequestCredentials,
)
from config import config
import handlers
import utils
from protocols import GenomicValidationRequest, HealthCheck

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔱 Initialize the Agent using the permanent environment seed
spartan_agent = Agent(
    name=os.getenv("AGENT_NAME", "spartan_bio_validate"),
    seed=os.getenv("AGENT_SEED_PHRASE"),
    endpoint=f"{os.getenv('RAILWAY_URL')}/endpoint"
)

@spartan_agent.on_event("startup")
async def on_startup(ctx: Context):
    logger.info(f"🔱 SPARTAN IDENTITY: {spartan_agent.address}")
    
    # 🔱 The Master Handshake: Registering the Proxy with Agentverse
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
        logger.info("✅ PROXY HANDSHAKE SUCCESSFUL - AGENTVERSE LINKED")
    except Exception as e:
        logger.error(f"❌ PROXY REGISTRATION FAILED: {e}")

@spartan_agent.on_message(model=GenomicValidationRequest)
async def handle_validation(ctx: Context, sender: str, msg: GenomicValidationRequest):
    logger.info(f"🧬 Ingesting Genomic Batch {msg.batch_id} from {sender}")
    response = await handlers.handle_genomic_validation_request(ctx, sender, msg)
    if response:
        await ctx.send(sender, response)

@spartan_agent.on_interval(period=60.0)
async def heartbeat(ctx: Context):
    logger.info("💓 [SPOPS HEARTBEAT] Proxy Mesh Nominal")

if __name__ == "__main__":
    # 🔱 Start the Proxy Server on Port 8000
    server = AgentServer(spartan_agent, host="0.0.0.0", port=8000)
    server.run()
