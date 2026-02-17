import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware  # ✅ This is required
# anthropic
from models import PromptRequest, ClaudeRequest, ClaudeResponse
from anthropic_client import ask_claude
# openai
from pydantic import BaseModel
from openai_service import generate_text

# numpy
# from numpy_service import array_sum, array_mean, dot_product

#pandas
# from pandas_service import create_dataframe, calculate_column_mean, filter_by_condition

# llama
from llama_service import LlamaService


# fitness api
from schemas import FitnessRequest, FitnessResponse
from ai_client import generate_fitness_plan

# Smart Research Assistant
import shutil
from services.document_processing import process_document
from services.graph_service import generate_concept_graph

#web-scrape
from web_scrape import scrape_multiple_urls

# common code
app = FastAPI()


# ✅ Allowed origins (Angular local + deployed frontend)
origins = [
    "http://localhost:4200",
    "https://melodious-phoenix-1af0bc.netlify.app",
]

# ✅ Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # specific frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST"],      # allowed HTTP methods
    allow_headers=["Content-Type", "Authorization"],  # allowed headers
)


 # Render provides this env var
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Render!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run(app, host="127.0.0.1", port=port)

    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}


# sample code
def greet(name, greeting="Hello"):
    """Function with default parameters"""
    return f"{greeting}, {name}!"

@app.get("/greet")
def greet_user(name: str, greeting: str = "Hello"):
    message = greet(name, greeting)
    return {"message": message}

# run app
# uvicorn main:app --reload

# http://127.0.0.1:8000/greet?name=Alice
# {"message": "Hello, Alice!"}

# http://127.0.0.1:8000/greet?name=Bob&greeting=Hi
# {"message": "Hi, Bob!"}




# anthropic function (accepts both prompt and message for frontend compatibility)
@app.post("/claude", response_model=ClaudeResponse)
async def ask_claude_api(request: ClaudeRequest):
    try:
        text = request.get_text()
        if not text:
            raise HTTPException(status_code=400, detail="Either 'prompt' or 'message' is required")
        result = ask_claude(text)
        return ClaudeResponse(response=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# openai function (uses PromptRequest from models)
@app.post("/openai/")
async def generate_endpoint(request: PromptRequest):
    response = generate_text(request.prompt)
    
    if response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response)
    
    return {"response": response}


# numpy
# class NumbersRequest(BaseModel):
#     numbers: list[float]

# class DotRequest(BaseModel):
#     a: list[float]
#     b: list[float]

# @app.post("/numpy-sum/")
# async def calculate_sum(request: NumbersRequest):
#     try:
#         result = array_sum(request.numbers)
#         return {"sum": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/numpy-mean/")
# async def calculate_mean(request: NumbersRequest):
#     try:
#         result = array_mean(request.numbers)
#         return {"mean": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/numpy-dot/")
# async def calculate_dot(request: DotRequest):
#     try:
#         result = dot_product(request.a, request.b)
#         return {"dot_product": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



#pandas
# class DataRequest(BaseModel):
#     data: list[dict]

# class ColumnRequest(BaseModel):
#     data: list[dict]
#     column: str

# class FilterRequest(BaseModel):
#     data: list[dict]
#     column: str
#     min_value: float

# @app.post("/pandas-dataframe/")
# async def get_dataframe(request: DataRequest):
#     try:
#         df = create_dataframe(request.data)
#         return {"dataframe": df.to_dict(orient="records")}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/pandas-mean/")
# async def get_mean(request: ColumnRequest):
#     try:
#         mean_value = calculate_column_mean(request.data, request.column)
#         return {"mean": mean_value}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/pandas-filter/")
# async def filter_data(request: FilterRequest):
#     try:
#         filtered = filter_by_condition(request.data, request.column, request.min_value)
#         return {"filtered_data": filtered}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    


# LlamaIndex service
llama_service = LlamaService(data_path="data")

@app.get("/llama_service/")
def root():
    return {"message": "LlamaIndex + FastAPI + PDF ready 🚀"}

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    user_query = data.get("query")
    
    if not user_query:
        return {"error": "No query provided."}

    answer = llama_service.query(user_query)
    return {"response": answer}


# fitness
@app.post("/fitness", response_model=FitnessResponse)
async def get_fitness_plan(request: FitnessRequest):
    try:
        result = generate_fitness_plan(request.dict())
        return FitnessResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Smart Research Assistant (Multimodal)
# tech stack: Backend: FastAPI, Frontend: Angular, AI Models: OpenAI GPT-4, 
#             Knowledge Graph: LangGraph, Orchestration/Logging: LangFuse / LangSmith
#             Visualization: Agno or D3.js in Angular
@app.post("/upload")
async def upload_file(file: UploadFile):
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Process document to get summary and graph
        summary, graph = process_document(temp_file_path)

        return {
            "summary": summary,
            "graph": graph
        }
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# Web scrape
class UrlListRequest(BaseModel):
    urls: list[str]

@app.post("/scrape-multiple")
async def scrape_multiple(data: UrlListRequest):
    return await scrape_multiple_urls(data.urls)
# ..