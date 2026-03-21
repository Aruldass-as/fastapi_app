from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.openai_service import generate_text
from app.services.anthropic_service import ask_claude

router = APIRouter()

class AIChatRequest(BaseModel):
    message: str
    provider: str = "openai"  # openai, claude, gemini
    model: str = None  # Optional specific model

class AIChatResponse(BaseModel):
    response: str
    provider: str
    model: str

@router.post("/ai/chat", response_model=AIChatResponse)
async def ai_chat(request: AIChatRequest):
    """Chat with various AI providers."""
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        provider = request.provider.lower()

        if provider == "openai":
            response = generate_text(request.message)
            model = request.model or "gpt-4o-mini"

        elif provider == "claude":
            response = ask_claude(request.message)
            model = request.model or "claude-3-opus-20240229"

        elif provider == "gemini":
            # Placeholder for Gemini
            response = f"Gemini placeholder response for: '{request.message[:50]}...'"
            model = request.model or "gemini-pro"

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")

        if response.startswith("Error:"):
            raise HTTPException(status_code=500, detail=response)

        return AIChatResponse(
            response=response,
            provider=provider,
            model=model
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
