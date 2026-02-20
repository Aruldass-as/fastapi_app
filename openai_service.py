# Project structure
# -------------------
# fastapi_app/
# │
# ├── main.py
# ├── openai_service.py
# ├── .env
# └── requirements.txt

# install
# ---------
# pip install fastapi uvicorn openai python-dotenv

# openai_service.py

import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def stream_chat(prompt: str):
    """Stream chat completion tokens as they arrive."""
    stream = await async_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def generate_text(prompt: str) -> str:
    """
    Generate a response from OpenAI based on the provided prompt.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # You can also use gpt-4o, gpt-4-turbo, etc.
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def generate_image(prompt: str) -> dict:
    """
    Generate an image from the prompt. Tries gpt-image-1-mini first (faster, better
    prompt following), falls back to DALL-E 3 if unavailable.
    Returns {"url": str} or {"b64_data_url": str} for display.
    """
    # Try gpt-image-1-mini first: ~2-10s, superior prompt following
    try:
        response = client.images.generate(
            model="gpt-image-1-mini",
            prompt=prompt.strip(),
            size="1024x1024",
            quality="low",  # fastest; use "medium" or "high" for better quality
        )
        data = response.data[0]
        b64 = getattr(data, "b64_json", None) or (data.model_dump() if hasattr(data, "model_dump") else {}).get("b64_json")
        if b64:
            return {"b64_data_url": f"data:image/png;base64,{b64}"}
        url = getattr(data, "url", None)
        if url:
            return {"url": url}
    except Exception as e:
        err_msg = str(e).lower()
        # Fall back to DALL-E 3 if gpt-image not available (e.g. org not verified)
        if "403" in err_msg or "not found" in err_msg or "organization" in err_msg:
            pass
        else:
            return {"error": f"Error: {str(e)}"}

    # Fallback: DALL-E 3 with quality=standard (faster) and style=natural (closer to prompt)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt.strip(),
            n=1,
            size="1024x1024",
            quality="standard",  # faster than "hd"
            style="natural",    # more literal prompt following, less creative rewriting
            response_format="url",
        )
        return {"url": response.data[0].url}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

