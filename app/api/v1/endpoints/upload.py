from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import os
import tempfile
from app.services.document_service import process_document

router = APIRouter()

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF document."""
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Process the document
            summary, graph = process_document(temp_file_path)

            return JSONResponse(content={
                "filename": file.filename,
                "summary": summary,
                "graph": graph,
                "status": "processed"
            })

        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
