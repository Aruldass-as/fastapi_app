# fastapi_app/
# │
# ├── main.py
# ├── matplotlib_service.py
# └── requirements.txt


# pip install fastapi uvicorn matplotlib


# matplotlib_service.py

import io
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse

def generate_line_chart(x_values: list[float], y_values: list[float]):
    """Generate a simple line chart."""
    plt.figure(figsize=(6, 4))
    plt.plot(x_values, y_values, marker='o')
    plt.title("Line Chart Example")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.grid(True)

    # Save chart to memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

def generate_bar_chart(categories: list[str], values: list[float]):
    """Generate a bar chart."""
    plt.figure(figsize=(6, 4))
    plt.bar(categories, values, color='skyblue')
    plt.title("Bar Chart Example")
    plt.xlabel("Categories")
    plt.ylabel("Values")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

def generate_pie_chart(labels: list[str], sizes: list[float]):
    """Generate a pie chart."""
    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Pie Chart Example")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")



# generate_line_chart:
# Answer:
# {
#   "x_values": [1, 2, 3, 4, 5],
#   "y_values": [10, 20, 15, 25, 30]
# }

# generate_bar_chart:
# Answer:
# {
#   "categories": ["A", "B", "C", "D"],
#   "values": [10, 25, 18, 30]
# }

# generate_pie_chart:
# Answer:
# {
#   "labels": ["Python", "JavaScript", "C++"],
#   "sizes": [45, 35, 20]
# }
