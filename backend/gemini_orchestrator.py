import os
from typing import Dict, Any
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = "gemini-3.1-pro"
        
        self.available_functions = {
            "get_dynamic_quote": {
                "description": "Calculate dynamic pricing for the 10M record Squeeze.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "record_count": {"type": "integer"},
                        "requires_lazarus": {"type": "boolean"},
                        "requires_fips": {"type": "boolean"}
                    },
                    "required": ["record_count"]
                }
            }
        }

    async def orchestrate_query(self, user_query: str) -> Dict[str, Any]:
        logger.info(f"Orchestrating query: {user_query}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "parts": [{"text": user_query}]}],
            "tools": [{"function_declarations": self.available_functions}]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

_gemini_orchestrator = None
def get_gemini_orchestrator(config: Dict[str, Any]) -> GeminiOrchestrator:
    global _gemini_orchestrator
    if _gemini_orchestrator is None:
        _gemini_orchestrator = GeminiOrchestrator(config)
    return _gemini_orchestrator
