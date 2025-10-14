from fastapi import FastAPI, HTTPException
# anthropic 
from models import PromptRequest, ClaudeResponse
from anthropic_client import ask_claude
# openai
from pydantic import BaseModel
from openai_service import generate_text

# numpy
from numpy_service import array_sum, array_mean, dot_product

#pandas
from pandas_service import create_dataframe, calculate_column_mean, filter_by_condition

# matplotlib 
from matplotlib_service import generate_line_chart, generate_bar_chart, generate_pie_chart

# seaborn
from seaborn_service import create_histogram, create_scatterplot, create_boxplot

# llama
from fastapi import FastAPI, Request
from llama_service import LlamaService


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

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI from VS Code!"}

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




# anthropic function
@app.post("/claude", response_model=ClaudeResponse)
async def ask_claude_api(request: PromptRequest):
    try:
        result = ask_claude(request.prompt)
        return ClaudeResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# openai function
class PromptRequest(BaseModel):
    prompt: str

@app.post("/openai/")
async def generate_endpoint(request: PromptRequest):
    response = generate_text(request.prompt)
    
    if response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response)
    
    return {"response": response}


# numpy
class NumbersRequest(BaseModel):
    numbers: list[float]

class DotRequest(BaseModel):
    a: list[float]
    b: list[float]

@app.post("/numpy-sum/")
async def calculate_sum(request: NumbersRequest):
    try:
        result = array_sum(request.numbers)
        return {"sum": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/numpy-mean/")
async def calculate_mean(request: NumbersRequest):
    try:
        result = array_mean(request.numbers)
        return {"mean": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/numpy-dot/")
async def calculate_dot(request: DotRequest):
    try:
        result = dot_product(request.a, request.b)
        return {"dot_product": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#pandas
class DataRequest(BaseModel):
    data: list[dict]

class ColumnRequest(BaseModel):
    data: list[dict]
    column: str

class FilterRequest(BaseModel):
    data: list[dict]
    column: str
    min_value: float

@app.post("/pandas-dataframe/")
async def get_dataframe(request: DataRequest):
    try:
        df = create_dataframe(request.data)
        return {"dataframe": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pandas-mean/")
async def get_mean(request: ColumnRequest):
    try:
        mean_value = calculate_column_mean(request.data, request.column)
        return {"mean": mean_value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pandas-filter/")
async def filter_data(request: FilterRequest):
    try:
        filtered = filter_by_condition(request.data, request.column, request.min_value)
        return {"filtered_data": filtered}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# matplotlib 
class LineChartRequest(BaseModel):
    x_values: list[float]
    y_values: list[float]

class BarChartRequest(BaseModel):
    categories: list[str]
    values: list[float]

class PieChartRequest(BaseModel):
    labels: list[str]
    sizes: list[float]

@app.post("/matplotlib-line-chart/")
async def line_chart(request: LineChartRequest):
    return generate_line_chart(request.x_values, request.y_values)

@app.post("/matplotlib-bar-chart/")
async def bar_chart(request: BarChartRequest):
    return generate_bar_chart(request.categories, request.values)

@app.post("/matplotlib-pie-chart/")
async def pie_chart(request: PieChartRequest):
    return generate_pie_chart(request.labels, request.sizes)


# seaborn
class HistogramRequest(BaseModel):
    data: list[float]
    bins: int = 10

class ScatterRequest(BaseModel):
    x: list[float]
    y: list[float]

class BoxPlotRequest(BaseModel):
    data: list[float]

@app.post("/seaborn-histogram/")
async def histogram_chart(request: HistogramRequest):
    return create_histogram(request.data, request.bins)

@app.post("/seaborn-scatter/")
async def scatter_chart(request: ScatterRequest):
    return create_scatterplot(request.x, request.y)

@app.post("/seaborn-boxplot/")
async def box_chart(request: BoxPlotRequest):
    return create_boxplot(request.data)


# LlamaIndex service
llama_service = LlamaService(data_path="data")

@app.get("/")
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