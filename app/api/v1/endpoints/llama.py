from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llama_service import LlamaService

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

# Initialize the Llama service lazily (only when first used)
llama_service = None

def get_llama_service():
    """Get or create LlamaService instance."""
    global llama_service
    if llama_service is None:
        try:
            llama_service = LlamaService()
        except ValueError as e:
            if "No files found" in str(e):
                raise HTTPException(
                    status_code=503,
                    detail="Document index not available. Please add PDF files to app/data/ directory and restart the server."
                )
            raise
    return llama_service

@router.post("/llama/query", response_model=dict)
async def query_documents(request: QueryRequest):
    """Query indexed documents using LlamaIndex."""
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        service = get_llama_service()
        result = service.query(request.query)
        return {"response": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
