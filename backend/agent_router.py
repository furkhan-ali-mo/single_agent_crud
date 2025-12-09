from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.llm import analyze_intent
from backend.agent import handle_agent_action

agent_router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: List[List[str]] = []
    
@agent_router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to handle user chat messages.
    1. Analyzes intent using LLM.
    2. Executes action via Agent Logic.
    3. Returns assistant response.
    """
    try:
        # 1. Analyze Intent
        structured_data = analyze_intent(request.message)
        
        # 2. Route & Execute
        response_text = await handle_agent_action(structured_data)
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
