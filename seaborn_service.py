# fastapi_app/
# │
# ├── main.py
# ├── seaborn_service.py
# └── requirements.txt

# pip install fastapi uvicorn seaborn matplotlib pandas


# seaborn_service.py

import io
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from fastapi.responses import StreamingResponse

def create_histogram(data: list[float], bins: int = 10):
    """Generate a histogram from numeric data."""
    plt.figure(figsize=(6, 4))
    sns.histplot(data, bins=bins, kde=True, color="skyblue")
    plt.title("Histogram")
    plt.xlabel("Values")
    plt.ylabel("Frequency")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


def create_scatterplot(x: list[float], y: list[float]):
    """Generate a scatter plot."""
    df = pd.DataFrame({"x": x, "y": y})
    plt.figure(figsize=(6, 4))
    sns.scatterplot(data=df, x="x", y="y", color="orange")
    plt.title("Scatter Plot")
    plt.xlabel("X Values")
    plt.ylabel("Y Values")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


def create_boxplot(data: list[float]):
    """Generate a box plot."""
    plt.figure(figsize=(5, 4))
    sns.boxplot(y=data, color="lightgreen")
    plt.title("Box Plot")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")



# create_histogram:
# {
#   "data": [10, 12, 13, 15, 18, 18, 19, 20, 21, 23, 25],
#   "bins": 5
# }

# create_scatterplot:
# {
#   "x": [1, 2, 3, 4, 5, 6],
#   "y": [2, 3.5, 4, 6, 7.5, 9]
# }

# create_boxplot:
# {
#   "data": [15, 18, 19, 22, 24, 30, 35, 45]
# }
