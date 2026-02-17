# Simple concept extraction + node creation using GPT
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_concept_graph(summary: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a data scientist."},
            {"role": "user", "content": f"Extract key concepts and relationships from the following text as JSON nodes and edges:\n{summary}"}
        ]
    )
    # Expect JSON output like: {"nodes": [...], "edges": [...]}
    import json
    import re
    content = response.choices[0].message.content or ""
    # Strip markdown code blocks if present
    content = re.sub(r"```(?:json)?\s*", "", content).strip()
    try:
        result = json.loads(content)
        if "nodes" in result and "edges" in result:
            return result
        return {"nodes": result.get("nodes", []), "edges": result.get("edges", [])}
    except json.JSONDecodeError:
        return {"nodes": [], "edges": []}
