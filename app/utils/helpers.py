# Utilities helper functions
import json
from typing import Any


def parse_json_response(content: str) -> dict:
    """Safely parse JSON from string content."""
    try:
        if isinstance(content, str):
            return json.loads(content)
        return content
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON: {content}"}


def validate_required_fields(data: dict, required_fields: list[str]) -> bool:
    """Validate that all required fields are present in data."""
    return all(field in data for field in required_fields)
