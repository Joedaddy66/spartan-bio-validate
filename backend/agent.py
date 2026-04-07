from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from gemini_orchestrator import get_gemini_orchestrator
import os

app = FastAPI(title="Spartan Bio-Validate API v7.0 OMEGA")

class QueryRequest(BaseModel):
    query: str
    frontend_context: Optional[Dict[str, Any]] = None

@app.get("/health")
async def health_check():
    return {"status": "GREEN", "version": "v7.0 OMEGA", "drift": "0.00%", "lazarus_protocol": "ACTIVE"}

@app.post("/gemini/orchestrate")
async def gemini_orchestrate(request: QueryRequest):
    try:
        config = {} 
        gemini = get_gemini_orchestrator(config)
        result = await gemini.orchestrate_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
