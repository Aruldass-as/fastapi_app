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
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

