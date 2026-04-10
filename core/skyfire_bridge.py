"""
SKYFIRE MARKETPLACE BRIDGE
Handles autonomous token verification and charging for AI agents.
"""

import os
import logging
from typing import Dict, Any, Optional
from skyfire import Skyfire
from jose import jwt
import aiohttp

logger = logging.getLogger(__name__)

class SkyfireBridge:
    """Utility to interface with the Skyfire.xyz protocol"""
    
    def __init__(self):
        self.api_key = os.getenv("SKYFIRE_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = Skyfire(api_key=self.api_key)
                logger.info("✅ Skyfire SDK initialized using SKYFIRE_API_KEY")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Skyfire SDK: {str(e)}")
        else:
            logger.warning("⚠️ SKYFIRE_API_KEY not found. Skyfire charging will be skipped.")

    async def verify_and_charge(self, token: str, amount_usd: float = 0.10) -> Dict[str, Any]:
        """
        Verify an incoming Skyfire PAY token and execute a charge.
        Called by the API Gateway when a Skyfire agent makes a request.
        """
        if not self.client:
            return {"success": False, "error": "Skyfire SDK not initialized"}

        try:
            # 1. Verify the token (using Skyfire's internal logic or JWKS)
            # In a real scenario, the SDK handles this check.
            # We assume 'token' is the 'X-Skyfire-Pay-Token' header value.
            
            logger.info(f"🪙 Attempting to charge Skyfire token for ${amount_usd:.2f}")
            
            # 2. Execute the charge
            # This captures real revenue from the buyer agent's Skyfire wallet
            charge_result = self.client.charge_token(
                token=token,
                amount=amount_usd,
                currency="USD",
                description="Spartan Bio-Validate: Genomic Sequence Validation"
            )
            
            if charge_result.get("status") == "success":
                logger.info(f"✅ Skyfire Charge Successful: {charge_result.get('transaction_id')}")
                return {"success": True, "transaction_id": charge_result.get("transaction_id")}
            else:
                logger.error(f"❌ Skyfire Charge Rejected: {charge_result.get('message')}")
                return {"success": False, "error": charge_result.get("message")}

        except Exception as e:
            logger.error(f"❌ Skyfire Bridge Error: {str(e)}")
            return {"success": False, "error": str(e)}

# Global instance
skyfire = SkyfireBridge()
