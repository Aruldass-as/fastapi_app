import asyncio
import json
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware  # ✅ This is required
from fastapi.responses import StreamingResponse
# anthropic
from models import PromptRequest, ClaudeRequest, ClaudeResponse
from anthropic_client import ask_claude
# openai
from pydantic import BaseModel
from openai_service import generate_text, generate_image, stream_chat

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


# Node.js API compatibility - chat (OpenAI)
class ChatRequest(BaseModel):
    message: str

async def _handle_chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    response = await asyncio.to_thread(generate_text, request.message)
    if response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response)
    return {"reply": response}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return await _handle_chat(request)

@app.post("/api/chat")  # Node.js path compatibility
async def api_chat_endpoint(request: ChatRequest):
    return await _handle_chat(request)


# Streaming chat - tokens stream as they arrive for faster perceived response
@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    async def generate():
        try:
            async for chunk in stream_chat(request.message):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


# Node.js API compatibility - generate-image (OpenAI DALL-E)
class ImageRequest(BaseModel):
    prompt: str

@app.post("/generate-image")
async def generate_image_endpoint(request: ImageRequest):
    result = await asyncio.to_thread(generate_image, request.prompt)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return {**result, "revised_prompt": request.prompt}


# Node.js API compatibility - gemini
class MessageRequest(BaseModel):
    message: str

@app.post("/gemini")
async def gemini_endpoint(request: MessageRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=501, detail="Add GOOGLE_API_KEY or GEMINI_API_KEY to fastapi_app/.env (get key from https://aistudio.google.com/apikey)")
    # Use REST API directly (no SDK dependency, more reliable)
    import json
    import urllib.request
    import urllib.error
    payload = {
        "contents": [{"parts": [{"text": request.message}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024}
    }
    last_error = None
    for model_id in ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-pro"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
            req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if text:
                return {"reply": text}
        except urllib.error.HTTPError as e:
            last_error = e.read().decode() if e.fp else str(e)
            if "404" in str(e) or "not found" in last_error.lower():
                continue
            if e.code == 429 or "quota" in last_error.lower() or "RESOURCE_EXHAUSTED" in last_error:
                raise HTTPException(status_code=429, detail="Gemini API quota exceeded. Wait a few minutes or check https://ai.google.dev/gemini-api/docs/rate-limits")
            raise HTTPException(status_code=e.code, detail=last_error[:500])
        except Exception as e:
            last_error = str(e)
            continue
    raise HTTPException(status_code=500, detail=last_error or "Gemini API failed")


# Node.js API compatibility - perplexity
@app.post("/perplexity")
async def perplexity_endpoint(request: MessageRequest):
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise HTTPException(status_code=501, detail="Set PERPLEXITY_API_KEY in .env")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
        response = client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{"role": "user", "content": request.message}],
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


# Node.js API compatibility - voice-chatbot (OpenAI Whisper + GPT + TTS)
@app.post("/voice-chatbot")
async def voice_chatbot(audio: UploadFile = File(...)):
    try:
        import io
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Read file into BytesIO (fixes SpooledTemporaryFile pointer issue with Whisper)
        audio_bytes = await audio.read()
        if not audio_bytes or len(audio_bytes) < 100:
            raise HTTPException(status_code=400, detail="Audio too short or empty. Record for at least 1 second.")
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = audio.filename or "audio.webm"
        # Speech to text
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        user_text = transcript.text
        # Generate response
        reply_text = generate_text(user_text)
        if reply_text.startswith("Error:"):
            raise HTTPException(status_code=500, detail=reply_text)
        # Text to speech
        tts = client.audio.speech.create(model="tts-1", voice="alloy", input=reply_text)
        import base64
        audio_base64 = base64.b64encode(tts.content).decode()
        return {"userText": user_text, "botReply": reply_text, "audioBase64": audio_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Node.js API compatibility - video generation (stub)
class VideoRequest(BaseModel):
    prompt: str

@app.post("/generate-video")
async def generate_video_endpoint(request: VideoRequest):
    raise HTTPException(
        status_code=501,
        detail="Video generation requires OpenAI Sora or similar API. Not yet implemented in FastAPI."
    )


@app.get("/video-status/{id}")
async def video_status(id: str):
    raise HTTPException(
        status_code=501,
        detail="Video status endpoint not yet implemented in FastAPI."
    )


# RAG compatibility - accept both query and question
@app.post("/api/query")
async def rag_query(request: Request):
    data = await request.json()
    user_query = data.get("query") or data.get("question")
    if not user_query:
        return {"error": "No query or question provided.", "reply": ""}
    answer = llama_service.query(user_query)
    return {"response": answer, "reply": answer}