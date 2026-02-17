from pydantic import BaseModel
from typing import Optional


class PromptRequest(BaseModel):
    prompt: str


class ClaudeRequest(BaseModel):
    """Accepts both 'prompt' and 'message' for frontend compatibility."""
    prompt: Optional[str] = None
    message: Optional[str] = None

    def get_text(self) -> str:
        return self.message or self.prompt or ""


class ClaudeResponse(BaseModel):
    response: str
