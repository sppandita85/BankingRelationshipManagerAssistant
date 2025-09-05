"""
FastAPI server for Banking RM Agent.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from banking_rm_agent.core.banking_rm_agent import BankingRMAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Banking RM Agent API",
    description="AI-powered Banking Relationship Manager Agent API",
    version="1.0.0"
)

# Initialize the agent
agent = BankingRMAgent()

# Pydantic models
class CustomerQuery(BaseModel):
    query: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    intent: str
    is_supported: bool
    customer_id: Optional[str]
    customer_name: Optional[str]
    timestamp: str
    query: str

class StatisticsResponse(BaseModel):
    total_queries: int
    supported_queries: int
    out_of_scope_queries: int
    support_rate: float
    intent_distribution: Dict[str, int]
    last_updated: str

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Banking RM Agent API",
        "version": "1.0.0",
        "status": "active"
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(customer_query: CustomerQuery):
    """
    Process a customer query through the Banking RM Agent.
    
    Args:
        customer_query: Customer query data
        
    Returns:
        Query response with intent classification and agent response
    """
    try:
        logger.info(f"Processing query: {customer_query.query}")
        
        result = agent.process_customer_query(
            customer_query=customer_query.query,
            customer_id=customer_query.customer_id,
            customer_name=customer_query.customer_name
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations", response_model=List[QueryResponse])
async def get_conversations(customer_id: Optional[str] = None):
    """
    Get conversation history.
    
    Args:
        customer_id: Optional customer ID to filter conversations
        
    Returns:
        List of conversation entries
    """
    try:
        conversations = agent.get_conversation_history(customer_id)
        return [QueryResponse(**conv) for conv in conversations]
        
    except Exception as e:
        logger.error(f"Error retrieving conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """
    Get agent performance statistics.
    
    Returns:
        Agent statistics including support rate and intent distribution
    """
    try:
        stats = agent.get_agent_statistics()
        return StatisticsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Error retrieving statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversations")
async def reset_conversations():
    """
    Reset conversation history.
    
    Returns:
        Success message
    """
    try:
        agent.reset_conversation_history()
        return {"message": "Conversation history reset successfully"}
        
    except Exception as e:
        logger.error(f"Error resetting conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agent_initialized": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
