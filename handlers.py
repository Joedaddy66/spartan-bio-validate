import logging
from uagents import Context
from protocols import GenomicValidationRequest, GenomicValidationResponse, HealthCheck, HealthResponse
from config import config
from utils import TimeUtils, RailwayClient, metrics

logger = logging.getLogger(__name__)

async def handle_genomic_validation_request(ctx: Context, sender: str, msg: GenomicValidationRequest) -> GenomicValidationResponse:
    logger.info(f"🧬 Processing validation request for batch {msg.batch_id} from {sender}")
    
    # 1. Calculate price based on Sovereign Broker logic
    record_count = len(msg.sequences)
    unit_cost = 0.10 # $0.10 base
    if msg.priority == "high":
        unit_cost = 0.30 # $0.30 Lazarus/High priority
    
    total_cost_usd = record_count * unit_cost
    logger.info(f"💰 Calculated cost for batch {msg.batch_id}: ${total_cost_usd:.2f}")

    # 2. Relay directly to the Railway Backend (api/gateway.py)
    async with RailwayClient(config.railway.url) as client:
        try:
            # We transform the agent message into the format the backend expects
            sequences_data = [
                {"sequence": s.sequence, "sequence_id": s.sequence_id} 
                for s in msg.sequences
            ]
            
            # The backend (/validate) will hand off to Celery
            result = await client.validate_sequences(
                batch_id=msg.batch_id,
                sequences=sequences_data,
                source_agent=sender,
                validation_options=msg.validation_options,
                priority=msg.priority
            )
            
            metrics.increment("validations_submitted")
            
            return GenomicValidationResponse(
                batch_id=msg.batch_id,
                status="success",
                job_id=result.get("job_id", f"gen_{msg.batch_id}"),
                message=f"Validation accepted. Total Cost: ${total_cost_usd:.2f}. Processing via unified gateway.",
                sequences_count=record_count,
                timestamp=TimeUtils.iso_timestamp(),
                Railway_url=config.railway.url
            )
        except Exception as e:
            logger.error(f"❌ Backend relay failed: {str(e)}")
            metrics.increment("errors")
            return GenomicValidationResponse(
                batch_id=msg.batch_id,
                status="error",
                job_id="failed",
                message=f"Backend relay error: {str(e)}",
                sequences_count=record_count,
                timestamp=TimeUtils.iso_timestamp(),
                Railway_url=config.railway.url
            )

async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck) -> HealthResponse:
    logger.info(f"🏥 Handling health check from {sender}")
    current_metrics = metrics.get()
    return HealthResponse(
        status="healthy",
        agent_name=config.agent.name,
        uptime=current_metrics.get("uptime_seconds", 0.0),
        metrics=current_metrics,
        capabilities=["genomic_validation", "autonomous_payments", "unified_gateway"],
        check_id=msg.check_id,
        timestamp=TimeUtils.iso_timestamp()
    )
