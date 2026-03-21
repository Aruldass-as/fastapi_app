from fastapi import APIRouter
from app.api.v1.endpoints import (
    openai, claude, gemini, llama, fitness, upload, scrape, voice, ai_chat
)

api_router = APIRouter()

api_router.include_router(openai.router)
api_router.include_router(claude.router)
api_router.include_router(gemini.router)
api_router.include_router(llama.router)
api_router.include_router(fitness.router)
api_router.include_router(upload.router)
api_router.include_router(scrape.router)
api_router.include_router(voice.router)
api_router.include_router(ai_chat.router)
