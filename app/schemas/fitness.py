from pydantic import BaseModel


class FitnessRequest(BaseModel):
    age: int
    gender: str
    goal: str
    fitness_level: str
    preferences: str | None = None


class FitnessResponse(BaseModel):
    workout_plan: str
    diet_plan: str
    tips: str
