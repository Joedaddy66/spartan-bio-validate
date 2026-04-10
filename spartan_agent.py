"""
SPARTAN BIO-VALIDATE MAIN AGENT (PROXY MODE)
"""

import logging
import uvicorn
from uagents import Agent, Context, AgentServer
from config import config
import handlers
import utils
from protocols import (
    GenomicValidationRequest,
    HealthCheck
)

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.monitoring.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# =====================================================================
# AGENT INITIALIZATION (PROXY MODE)
# =====================================================================

# CRITICAL: Initialize agent with endpoint for Proxy Mode
spartan_agent = Agent(
    name=config.agent.name,
    seed=config.agent.seed,
    endpoint=config.proxy.endpoint if config.proxy.enabled else None
)

logger.info("=" * 60)
logger.info("🔱 SPARTAN BIO-VALIDATE AGENT STARTING (PROXY MODE)...")
logger.info(f"👑 Agent Name: {config.agent.name}")
logger.info(f"🔑 Agent Address: {spartan_agent.address}")
logger.info(f"🌐 Proxy Mode: {config.proxy.enabled}")
if config.proxy.enabled:
    logger.info(f"🌐 Proxy Endpoint: {config.proxy.endpoint}")
logger.info(f"🎯 Railway Backend: {config.railway.url}")
logger.info("=" * 60)

# =====================================================================
# MESSAGE HANDLERS
# =====================================================================

@spartan_agent.on_message(model=GenomicValidationRequest)
async def handle_validation_request(
    ctx: Context,
    sender: str,
    msg: GenomicValidationRequest
):
    """Handle genomic validation requests"""
    logger.info(f"🧬 Received validation request from {sender}")
    response = await handlers.handle_genomic_validation_request(ctx, sender, msg)
    if response:
        await ctx.send(sender, response)
        logger.info(f"✅ Validation response sent to {sender}")

@spartan_agent.on_message(model=HealthCheck)
async def handle_health_check(
    ctx: Context,
    sender: str,
    msg: HealthCheck
):
    """Handle health check requests"""
    logger.info(f"🏥 Health check from {sender}")
    response = await handlers.handle_health_check(ctx, sender, msg)
    await ctx.send(sender, response)

# =====================================================================
# AGENT LIFECYCLE
# =====================================================================

@spartan_agent.on_event("startup")
async def on_startup(ctx: Context):
    """Agent startup handler"""
    logger.info("=" * 60)
    logger.info("🚀 SPARTAN AGENT STARTUP COMPLETE")
    logger.info("=" * 60)

    utils.registry.register(
        spartan_agent.address,
        {
            "agent_address": spartan_agent.address,
            "agent_name": config.agent.name,
            "endpoint": config.proxy.endpoint if config.proxy.enabled else None,
            "capabilities": [
                "genomic_validation",
                "health_monitoring",
                "metrics_tracking"
            ]
        }
    )

@spartan_agent.on_interval(period=config.monitoring.heartbeat_interval)
async def heartbeat(ctx: Context):
    """Periodic heartbeat"""
    uptime = utils.metrics.get()['uptime_seconds']
    logger.info(f"💓 [HEARTBEAT] Uptime: {uptime:.1f}s")

@spartan_agent.on_event("shutdown")
async def on_shutdown(ctx: Context):
    """Agent shutdown handler"""
    logger.info("=" * 60)
    logger.info("🛑 SPARTAN AGENT SHUTDOWN (PROXY MODE)")
    logger.info("=" * 60)

    final_metrics = utils.metrics.get()
    logger.info(f"📊 Final Metrics:")
    logger.info(f"   Messages Received: {final_metrics['messages_received']}")
    logger.info(f"   Messages Sent: {final_metrics['messages_sent']}")
    logger.info(f"   Validations Submitted: {final_metrics['validations_submitted']}")
    logger.info(f"   Errors: {final_metrics['errors']}")
    logger.info("=" * 60)

# =====================================================================
# MAIN ENTRY POINT - PROXY MODE SERVER
# =====================================================================

def run_proxy_mode():
    """
    Run the agent in Proxy Mode using AgentServer
    This exposes the agent via HTTP endpoint for Agentverse
    """
    try:
        logger.info("=" * 60)
        logger.info("🌐 STARTING PROXY MODE SERVER")
        logger.info("=" * 60)
        logger.info(f"✅ Agent Address: {spartan_agent.address}")
        logger.info(f"✅ Endpoint: {config.proxy.endpoint or 'internal mode'}")
        logger.info(f"✅ Host: {config.proxy.host}")
        logger.info(f"✅ Port: {config.proxy.port}")
        logger.info("=" * 60)

        if config.proxy.enabled:
            # Use AgentServer for Proxy Mode
            server = AgentServer(
                agent=spartan_agent,
                host=config.proxy.host,
                port=config.proxy.port
            )
            logger.info("🚀 AgentServer created for proxy mode")
            server.run()
        else:
            # Local mode without proxy
            logger.info("🔷 Running in local mode without proxy")
            spartan_agent.run()

    except KeyboardInterrupt:
        logger.info("👋 Agent stopped by user")
    except Exception as e:
        logger.error(f"❌ Agent crashed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    run_proxy_mode()
