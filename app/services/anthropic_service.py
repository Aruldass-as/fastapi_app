import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

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
