from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.scrape_service import scrape_multiple_urls

router = APIRouter()

class ScrapeRequest(BaseModel):
    urls: List[str]

class ScrapeResponse(BaseModel):
    success: bool
    count: int
    results: List[dict]

@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_urls(request: ScrapeRequest):
    """Scrape multiple URLs and extract structured data using AI."""
    try:
        if not request.urls or len(request.urls) == 0:
            raise HTTPException(status_code=400, detail="URLs list cannot be empty")

        if len(request.urls) > 10:  # Limit to prevent abuse
            raise HTTPException(status_code=400, detail="Maximum 10 URLs allowed per request")

        result = await scrape_multiple_urls(request.urls)
        return ScrapeResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
