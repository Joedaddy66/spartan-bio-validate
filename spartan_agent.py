import logging
from uagents import Agent, Context, AgentServer
from config import config
import handlers
import utils
from protocols import GenomicValidationRequest, HealthCheck

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

spartan_agent = Agent(
    name=config.agent.name,
    seed=config.agent.seed,
    endpoint=config.proxy.endpoint if config.proxy.enabled else None
)

@spartan_agent.on_message(model=GenomicValidationRequest)
async def handle_validation_request(ctx: Context, sender: str, msg: GenomicValidationRequest):
    logger.info(f"🧬 Received validation request from {sender}")
    response = await handlers.handle_genomic_validation_request(ctx, sender, msg)
    if response:
        await ctx.send(sender, response)

@spartan_agent.on_message(model=HealthCheck)
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    response = await handlers.handle_health_check(ctx, sender, msg)
    await ctx.send(sender, response)

@spartan_agent.on_interval(period=60.0)
async def heartbeat(ctx: Context):
    logger.info(f"💓 [SPOPS HEARTBEAT] Proxy Mesh Active")

if __name__ == "__main__":
    server = AgentServer(spartan_agent, host="0.0.0.0", port=8000)
    server.run()
