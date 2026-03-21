import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_V1_PREFIX = "/api/v1"

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# CORS Origins
CORS_ORIGINS = [
    "http://localhost:4200",
    "https://melodious-phoenix-1af0bc.netlify.app",
]

# Server configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
