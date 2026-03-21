from fastapi import APIRouter
from app.schemas.ai import ClaudeRequest, ClaudeResponse
from app.services.anthropic_service import ask_claude

router = APIRouter()

@router.post("/claude", response_model=ClaudeResponse)
async def ask_claude_api(request: ClaudeRequest):
    try:
        text = request.get_text()
        if not text:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Prompt required")
        result = ask_claude(text)
        return ClaudeResponse(response=result)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))
