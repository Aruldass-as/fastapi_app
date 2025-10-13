# Project structure
# -------------------
# fastapi_app/
# │
# ├── main.py              # Entry point (runs FastAPI app)
# ├── anthropic_client.py  # Anthropic API logic (Claude)
# ├── models.py            # Pydantic models
# └── requirements.txt 


# install
# ---------
# pip install fastapi uvicorn anthropic python-dotenv

# Requirements:
# ---------------
# Package	     Purpose
# fastapi	     --> The main web framework for creating APIs
# uvicorn	     --> ASGI server to run your FastAPI app
# anthropic	     --> Official Anthropic SDK to use Claude API
# python-dotenv	 --> Loads your .env file for ANTHROPIC_API_KEY



import os
import anthropic
from dotenv import load_dotenv

load_dotenv()  # load .env file if present

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_claude(prompt: str, model: str = "claude-3-opus-20240229") -> str:
    """Send a message to Claude and return its response."""
    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text
