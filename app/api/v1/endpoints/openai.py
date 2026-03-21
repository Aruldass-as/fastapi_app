from fastapi import APIRouter, HTTPException
from app.services.openai_service import generate_text, generate_image
from app.schemas.common import PromptRequest
from app.schemas.ai import ChatRequest

router = APIRouter()

# OpenAI text generation endpoint
@router.post("/openai/", response_model=dict)
async def generate_endpoint(request: PromptRequest):
    """Generate text using OpenAI GPT."""
    response = generate_text(request.prompt)

    if response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response)

    return {"response": response}

# OpenAI chat endpoint (Node.js API compatibility)
@router.post("/openai/chat", response_model=dict)
async def chat_endpoint(request: ChatRequest):
    """Chat with OpenAI GPT."""
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    response = generate_text(request.message)
    if response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response)

    return {"reply": response}

# OpenAI image generation endpoint
@router.post("/openai/image", response_model=dict)
async def image_endpoint(request: PromptRequest):
    """Generate image using OpenAI DALL-E."""
    result = generate_image(request.prompt)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result
