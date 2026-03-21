from fastapi import FastAPI
from app.core.cors import add_cors
from app.core.config import API_V1_PREFIX
from app.api.v1.api import api_router

app = FastAPI(
    title="Code Craft API",
    description="AI-powered API with OpenAI, Claude, Gemini, and Llama support",
    version="1.0.0"
)

# Add CORS middleware
add_cors(app)

# Include API routes
app.include_router(api_router, prefix=API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "message": "FastAPI running 🚀",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }
