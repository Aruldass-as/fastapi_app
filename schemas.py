from pydantic import BaseModel

class FitnessRequest(BaseModel):
    age: int
    gender: str
    goal: str  # e.g., "weight loss", "muscle gain"
    fitness_level: str  # e.g., "beginner", "intermediate"
    preferences: str | None = None  # e.g., "no equipment, vegetarian diet"

class FitnessResponse(BaseModel):
    workout_plan: str
    diet_plan: str
    tips: str
