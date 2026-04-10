import logging
from uagents import Agent, Context, AgentServer
from config import config
import handlers
import utils
from protocols import GenomicValidationRequest, HealthCheck

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize agent with Proxy Endpoint from Config
spartan_agent = Agent(
    name=config.agent.name,
    seed=config.agent.seed,
    endpoint=config.proxy.endpoint if config.proxy.enabled else None
)

@spartan_agent.on_event("startup")
async def on_startup(ctx: Context):
    logger.info(f"🔱 SPARTAN PROXY ACTIVE: {spartan_agent.address}")
    logger.info(f"🌐 PROXY ENDPOINT: {config.proxy.endpoint}")

@spartan_agent.on_message(model=GenomicValidationRequest)
async def handle_validation(ctx: Context, sender: str, msg: GenomicValidationRequest):
    logger.info(f"🧬 Ingesting Batch {msg.batch_id} from {sender}")
    response = await handlers.handle_genomic_validation_request(ctx, sender, msg)
    if response:
        await ctx.send(sender, response)

@spartan_agent.on_interval(period=60.0)
async def heartbeat(ctx: Context):
    logger.info("💓 [SPOPS HEARTBEAT] Proxy Mesh Nominal")

if __name__ == "__main__":
    server = AgentServer(spartan_agent, host="0.0.0.0", port=8000)
    server.run()
