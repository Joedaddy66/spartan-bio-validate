import logging
from uagents import Context
from protocols import GenomicValidationRequest, GenomicValidationResponse, HealthCheck, HealthResponse
from config import config
from utils import TimeUtils

logger = logging.getLogger(__name__)

async def handle_genomic_validation_request(ctx: Context, sender: str, msg: GenomicValidationRequest) -> GenomicValidationResponse:
    logger.info(f"Handling validation request for batch {msg.batch_id} from {sender}")
    return GenomicValidationResponse(
        batch_id=msg.batch_id,
        status="processing",
        job_id=f"job_{msg.batch_id}",
        message="Request received and proxy relay started.",
        sequences_count=len(msg.sequences),
        timestamp=TimeUtils.iso_timestamp(),
        Railway_url=config.railway.url
    )

async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck) -> HealthResponse:
    from utils import metrics
    logger.info(f"Handling health check from {sender}")
    return HealthResponse(
        status="healthy",
        agent_name=config.agent.name,
        uptime=metrics.get().get("uptime_seconds", 0.0),
        metrics=metrics.get(),
        capabilities=["genomic_validation", "health_monitoring", "metrics_tracking"],
        check_id=msg.check_id,
        timestamp=TimeUtils.iso_timestamp()
    )
