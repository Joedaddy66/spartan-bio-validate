"""
SPARTAN CONFIGURATION MANAGER WITH PROXY MODE SUPPORT
"""

import os
from typing import Dict
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AgentConfig:
    """Agent configuration"""
    name: str
    seed: str
    address: str
    host: str
    port: int
    proxy_mode: bool
    endpoint: str
    
    @classmethod
    def from_env(cls):
        railway_url = os.getenv("RAILWAY_URL", "")
        proxy_enabled = os.getenv("PROXY_MODE_ENABLED", "true").lower() == "true"
        
        return cls(
            name=os.getenv("AGENT_NAME", "spartan_bio_validate"),
            seed=os.getenv("AGENT_SEED", "spartan_overseer_spops_secure_seed_20260409"),
            address=os.getenv("AGENT_ADDRESS", ""),
            host=os.getenv("AGENT_HOST", "0.0.0.0"),
            port=int(os.getenv("AGENT_PORT", "8000")),
            proxy_mode=proxy_enabled,
            endpoint=f"{railway_url}/endpoint" if proxy_enabled else ""
        )

@dataclass
class RailwayConfig:
    """Railway backend configuration"""
    url: str
    validate_endpoint: str
    health_endpoint: str
    timeout: int
    
    @classmethod
    def from_env(cls):
        return cls(
            url=os.getenv("RAILWAY_URL", ""),
            validate_endpoint=os.getenv("RAILWAY_VALIDATE_ENDPOINT", "/validate"),
            health_endpoint=os.getenv("RAILWAY_HEALTH_ENDPOINT", "/health"),
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30"))
        )

@dataclass
class ProxyConfig:
    """Proxy mode configuration"""
    enabled: bool
    endpoint: str
    host: str
    port: int
    
    @classmethod
    def from_env(cls):
        railway_url = os.getenv("RAILWAY_URL", "")
        port = int(os.getenv("AGENT_PORT", "8000"))
        
        return cls(
            enabled=os.getenv("PROXY_MODE_ENABLED", "true").lower() == "true",
            endpoint=f"{railway_url}/endpoint",
            host=os.getenv("AGENT_HOST", "0.0.0.0"),
            port=port
        )

@dataclass
class MonitoringConfig:
    """Monitoring configuration"""
    heartbeat_interval: float
    log_level: str
    enable_metrics: bool
    
    @classmethod
    def from_env(cls):
        return cls(
            heartbeat_interval=float(os.getenv("HEARTBEAT_INTERVAL", "60.0")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            enable_metrics=os.getenv("ENABLE_METRICS", "true").lower() == "true"
        )

@dataclass
class SecurityConfig:
    """Security configuration"""
    encryption_enabled: bool
    api_key_header: str
    api_secret: str
    
    @classmethod
    def from_env(cls):
        return cls(
            encryption_enabled=os.getenv("ENCRYPTION_ENABLED", "true").lower() == "true",
            api_key_header=os.getenv("API_KEY_HEADER", "X-API-Key"),
            api_secret=os.getenv("API_SECRET", "spartan_secure_secret_key_v1")
        )

@dataclass
class PerformanceConfig:
    """Performance configuration"""
    max_batch_size: int
    max_retries: int
    request_timeout: int
    
    @classmethod
    def from_env(cls):
        return cls(
            max_batch_size=int(os.getenv("MAX_BATCH_SIZE", "100")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30"))
        )

class Config:
    """Master configuration class"""
    
    def __init__(self):
        self.agent = AgentConfig.from_env()
        self.railway = RailwayConfig.from_env()
        self.proxy = ProxyConfig.from_env()
        self.monitoring = MonitoringConfig.from_env()
        self.security = SecurityConfig.from_env()
        self.performance = PerformanceConfig.from_env()

config = Config()
