# fastapi_app/
# │
# ├── main.py
# ├── pandas_service.py
# └── requirements.txt

# pip install fastapi uvicorn pandas


# pandas_service.py

# import pandas as pd

# def create_dataframe(data: list[dict]) -> pd.DataFrame:
#     """
#     Convert a list of dictionaries into a Pandas DataFrame.
#     """
#     df = pd.DataFrame(data)
#     return df

# def calculate_column_mean(data: list[dict], column: str) -> float:
#     """
#     Calculate the mean of a specified numeric column.
#     """
#     df = pd.DataFrame(data)
#     if column not in df.columns:
#         raise ValueError(f"Column '{column}' not found.")
#     return df[column].mean()

# def filter_by_condition(data: list[dict], column: str, min_value: float) -> list[dict]:
#     """
#     Filter rows where column >= min_value.
#     """
#     df = pd.DataFrame(data)
#     if column not in df.columns:
#         raise ValueError(f"Column '{column}' not found.")
#     filtered_df = df[df[column] >= min_value]
#     return filtered_df.to_dict(orient="records")

# create_dataframe
# Question:
# {
#   "data": [
#     {"name": "Alice", "age": 25, "salary": 5000},
#     {"name": "Bob", "age": 30, "salary": 6000}
#   ]
# }
# Answer:
# {
#   "dataframe": [
#     {"name": "Alice", "age": 25, "salary": 5000},
#     {"name": "Bob", "age": 30, "salary": 6000}
#   ]
# }


# calculate_column_mean
# Question:
# {
#   "data": [
#     {"name": "Alice", "age": 25},
#     {"name": "Bob", "age": 35},
#     {"name": "Charlie", "age": 45}
#   ],
#   "column": "age"
# }
# Answer:
# {
#   "mean": 35.0
# }

# filter_by_condition
# Question:
# {
#   "data": [
#     {"name": "Alice", "age": 25},
#     {"name": "Bob", "age": 30},
#     {"name": "Charlie", "age": 45}
#   ],
#   "column": "age",
#   "min_value": 30
# }

# Answer:
# {
#   "filtered_data": [
#     {"name": "Bob", "age": 30},
#     {"name": "Charlie", "age": 45}
#   ]
# }
