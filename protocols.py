"""
SPARTAN MESSAGE PROTOCOLS
"""

from uagents import Model
from typing import List, Dict, Optional, Any
from pydantic import Field
from datetime import datetime

class GenomicSequence(Model):
    """Individual genomic sequence"""
    sequence: str = Field(..., description="Genomic sequence string")
    sequence_id: Optional[str] = Field(None, description="Sequence identifier")
    sequence_type: str = Field("DNA", description="DNA or RNA")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Sequence metadata")

class GenomicValidationRequest(Model):
    """Request for genomic sequence validation"""
    batch_id: str = Field(..., description="Batch identifier")
    sequences: List[GenomicSequence] = Field(..., description="Sequences to validate")
    source_agent: str = Field(..., description="Requesting agent address")
    validation_options: Optional[Dict[str, Any]] = Field(None, description="Options")
    priority: str = Field("normal", description="Priority level")

class GenomicValidationResponse(Model):
    """Response after validation submission"""
    batch_id: str = Field(..., description="Batch identifier")
    status: str = Field(..., description="Status")
    job_id: str = Field(..., description="Job ID")
    message: str = Field(..., description="Status message")
    sequences_count: int = Field(..., description="Number of sequences")
    timestamp: str = Field(..., description="Response timestamp")
    Railway_url: str = Field(..., description="Railway endpoint")

class HealthCheck(Model):
    """Health check request"""
    check_type: str = Field("general", description="Type of health check")
    check_id: str = Field(default_factory=lambda: f"health_{datetime.utcnow().timestamp()}")

class HealthResponse(Model):
    """Health check response"""
    status: str = Field(..., description="Status: healthy, degraded, error")
    agent_name: str = Field(..., description="Agent name")
    uptime: float = Field(..., description="Uptime in seconds")
    metrics: Dict[str, Any] = Field(..., description="Agent metrics")
    capabilities: List[str] = Field(..., description="Agent capabilities")
    check_id: str = Field(..., description="Corresponding check ID")
    timestamp: str = Field(..., description="Response timestamp")

class DatabaseStoreRequest(Model):
    """Request to store data in database"""
    collection: str = Field(..., description="Database collection")
    data: Dict[str, Any] = Field(..., description="Data to store")

class DatabaseStoreResponse(Model):
    """Response from database store"""
    status: str = Field(..., description="Storage status")
    document_id: str = Field(..., description="Document ID")
    timestamp: str = Field(..., description="Storage timestamp")

class DatabaseRetrieveRequest(Model):
    """Request to retrieve from database"""
    collection: str = Field(..., description="Database collection")
    query: Dict[str, Any] = Field(..., description="Query parameters")
    limit: int = Field(10, description="Number of results")

class DatabaseRetrieveResponse(Model):
    """Response from database retrieve"""
    status: str = Field(..., description="Retrieval status")
    documents: List[Dict[str, Any]] = Field(..., description="Retrieved documents")
    timestamp: str = Field(..., description="Retrieval timestamp")
