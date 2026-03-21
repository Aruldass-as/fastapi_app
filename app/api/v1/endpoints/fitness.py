from fastapi import APIRouter, HTTPException
from app.services.fitness_service import generate_fitness_plan
from app.schemas.fitness import FitnessRequest, FitnessResponse

router = APIRouter()

@router.post("/fitness", response_model=FitnessResponse)
async def fitness_plan_endpoint(request: FitnessRequest):
    """Generate personalized fitness plan using AI."""
    try:
        result = generate_fitness_plan({
            "age": request.age,
            "gender": request.gender,
            "goal": request.goal,
            "fitness_level": request.fitness_level,
            "preferences": request.preferences
        })

        return FitnessResponse(
            workout_plan=result.get("workout_plan", ""),
            diet_plan=result.get("diet_plan", ""),
            tips=result.get("tips", "")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
