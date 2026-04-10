import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    class agent:
        name = os.getenv("AGENT_NAME", "spartan_bio_validate")
        seed = os.getenv("AGENT_SEED", "spartan_overseer_spops_secure_seed_2026")
    
    class proxy:
        enabled = os.getenv("PROXY_MODE_ENABLED", "true").lower() == "true"
        # Builds the /endpoint URL for Agentverse to talk to Railway
        endpoint = f"{os.getenv('RAILWAY_URL')}/endpoint"
        host = "0.0.0.0"
        port = int(os.getenv("PORT", 8000))

    class railway:
        url = os.getenv("RAILWAY_URL")
        validate_endpoint = "/validate"

config = Config()
