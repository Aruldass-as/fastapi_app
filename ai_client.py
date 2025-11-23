import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_fitness_plan(request: dict) -> dict:
    prompt = f"""
You are an expert health & fitness coach.

Generate a structured fitness plan.

Input:
Age: {request['age']}
Gender: {request['gender']}
Goal: {request['goal']}
Fitness Level: {request['fitness_level']}
Preferences: {request.get('preferences', 'None')}

Return ONLY valid JSON with this format:

{{
  "workout_plan": "string",
  "diet_plan": "string",
  "tips": "string"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    # Extract text from model
    content = response.choices[0].message.content.strip()

    # Convert text to JSON safely
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fix formatting if model responded with extra text
        cleaned = content[
            content.find("{") : content.rfind("}") + 1
        ]
        data = json.loads(cleaned)

    return data
