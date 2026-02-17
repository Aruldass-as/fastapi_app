import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_fitness_plan(data: dict) -> dict:
    """Generate fitness plan using OpenAI based on user inputs."""
    prompt = f"""Create a personalized fitness plan for:
- Age: {data.get('age', 'N/A')}
- Gender: {data.get('gender', 'N/A')}
- Goal: {data.get('goal', 'N/A')}
- Fitness level: {data.get('fitness_level', 'N/A')}
- Preferences: {data.get('preferences', 'None')}

Return a JSON object with exactly these keys:
- workout_plan: string (detailed workout plan)
- diet_plan: string (diet recommendations)
- tips: string (general fitness tips)
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a fitness coach. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        import json
        content = response.choices[0].message.content
        result = json.loads(content) if isinstance(content, str) else content
        return {
            "workout_plan": result.get("workout_plan", ""),
            "diet_plan": result.get("diet_plan", ""),
            "tips": result.get("tips", "")
        }
    except Exception as e:
        return {
            "workout_plan": f"Error generating plan: {str(e)}",
            "diet_plan": "",
            "tips": ""
        }
