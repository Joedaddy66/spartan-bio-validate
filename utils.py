"""
SPARTAN UTILITY FUNCTIONS
"""

import aiohttp
import logging
from typing import Dict, Optional, Any
from datetime import datetime
from config import config

logger = logging.getLogger(__name__)

class TimeUtils:
    """Time-related utilities"""
    
    @staticmethod
    def iso_timestamp() -> str:
        """Get current ISO timestamp"""
        return datetime.utcnow().isoformat()
    
    @staticmethod
    def timestamp_now() -> float:
        """Get current timestamp"""
        return datetime.utcnow().timestamp()

class MetricsCollector:
    """Collect and track metrics"""
    
    def __init__(self):
        self.metrics = {
            "messages_received": 0,
            "messages_sent": 0,
            "validations_submitted": 0,
            "validations_completed": 0,
            "errors": 0,
            "start_time": TimeUtils.iso_timestamp()
        }
    
    def increment(self, metric_name: str, value: int = 1):
        """Increment a metric"""
        if metric_name in self.metrics:
            self.metrics[metric_name] += value
        else:
            self.metrics[metric_name] = value
    
    def get(self) -> Dict[str, Any]:
        """Get current metrics"""
        elapsed = TimeUtils.timestamp_now() - TimeUtils.parse_timestamp(self.metrics["start_time"]).timestamp()
        
        return {
            **self.metrics,
            "uptime_seconds": elapsed,
            "timestamp": TimeUtils.iso_timestamp()
        }
    
    @staticmethod
    def parse_timestamp(timestamp: str) -> datetime:
        """Parse ISO timestamp"""
        return datetime.fromisoformat(timestamp)

class AgentRegistry:
    """Track agent connections and capabilities"""
    
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}
    
    def register(self, agent_address: str, agent_info: Dict[str, Any]):
        """Register an agent"""
        self.agents[agent_address] = {
            **agent_info,
            "registered_at": TimeUtils.iso_timestamp(),
            "last_seen": TimeUtils.iso_timestamp()
        }
        logger.info(f"✅ Registered agent: {agent_address}")
    
    def update_heartbeat(self, agent_address: str):
        """Update agent last seen time"""
        if agent_address in self.agents:
            self.agents[agent_address]["last_seen"] = TimeUtils.iso_timestamp()
    
    def get_agent(self, agent_address: str) -> Optional[Dict[str, Any]]:
        """Get agent info"""
        return self.agents.get(agent_address)
    
    def get_all(self) -> list:
        """Get all registered agents"""
        return list(self.agents.values())

class RailwayClient:
    """HTTP client for Railway backend"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def validate_sequences(self, batch_id: str, sequences: list, source_agent: str, validation_options: Optional[Dict] = None, priority: str = "normal") -> Dict[str, Any]:
        """Submit validation request to Railway"""
        url = f"{self.base_url}{config.railway.validate_endpoint}"
        
        payload = {
            "batch_id": batch_id,
            "sequences": sequences,
            "source_agent": source_agent,
            "validation_options": validation_options or {},
            "priority": priority
        }
        
        headers = {"Content-Type": "application/json"}
        
        if config.security.encryption_enabled:
            headers[config.security.api_key_header] = config.security.api_secret
        
        try:
            async with self.session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Validation submitted: {batch_id}")
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Validation failed: {response.status} - {error_text}")
                    raise Exception(f"Validation failed: {response.status}")
        except Exception as e:
            logger.error(f"❌ Railway client error: {str(e)}")
            raise

class SequenceValidator:
    """Genomic sequence validator"""
    
    @staticmethod
    def validate_dna_sequence(sequence: str, max_length: int = 100000) -> Dict[str, Any]:
        """Validate DNA sequence format"""
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        if not sequence:
            result["valid"] = False
            result["errors"].append("Sequence is empty")
            return result
        
        if len(sequence) > max_length:
            result["valid"] = False
            result["errors"].append(f"Sequence exceeds maximum length of {max_length}")
        
        valid_bases = set('ATCGN')
        sequence_upper = sequence.upper()
        invalid_chars = set(sequence_upper) - valid_bases
        
        if invalid_chars:
            result["valid"] = False
            result["errors"].append(f"Invalid characters detected: {', '.join(sorted(invalid_chars))}")
        
        n_count = sequence_upper.count('N')
        if n_count > 0:
            percent_ambiguous = (n_count / len(sequence)) * 100
            if percent_ambiguous > 10:
                result["warnings"].append(f"High ambiguous content: {percent_ambiguous:.1f}% N bases")
        
        return result
    
    @staticmethod
    def validate_batch(sequences: list, max_batch_size: int = 100, max_sequence_length: int = 100000) -> Dict[str, Any]:
        """Validate batch of sequences"""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "results": []
        }
        
        if len(sequences) > max_batch_size:
            result["valid"] = False
            result["errors"].append(f"Batch exceeds maximum size of {max_batch_size}")
            return result
        
        for i, seq_data in enumerate(sequences):
            sequence = seq_data.get("sequence", "")
            validation = SequenceValidator.validate_dna_sequence(sequence, max_sequence_length)
            result["results"].append({
                "index": i,
                "sequence_id": seq_data.get("sequence_id"),
                **validation
            })
            
            if not validation["valid"]:
                result["valid"] = False
                result["errors"].append(f"Sequence {i}: {', '.join(validation['errors'])}")
        
        return result

# Global instances
metrics = MetricsCollector()
registry = AgentRegistry()
