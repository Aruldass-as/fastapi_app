# fastapi_app/
# │
# ├── main.py
# ├── numpy_service.py
# └── requirements.txt


# install
# ---------
# pip install fastapi uvicorn numpy


# numpy_service.py
# import numpy as np

# def array_sum(numbers: list) -> float:
#     """Return the sum of numbers."""
#     arr = np.array(numbers)
#     return np.sum(arr)

# def array_mean(numbers: list) -> float:
#     """Return the mean of numbers."""
#     arr = np.array(numbers)
#     return np.mean(arr)

# def dot_product(a: list, b: list) -> float:
#     """Return the dot product of two lists."""
#     arr1 = np.array(a)
#     arr2 = np.array(b)
#     return np.dot(arr1, arr2)




# array_sum
# Question:
# {
#   "numbers": [1, 2, 3, 4, 5]
# }
# Answer:
# {
#   "sum": 15.0
# }


# array_mean:
# Question:
# {
#   "numbers": [10, 20, 30, 40]
# }
# Answer:
# {
#   "mean": 25.0
# }


# dot_product
# Question:
# {
#   "a": [1, 2, 3],
#   "b": [4, 5, 6]
# }
# Answer:
# {
#   "dot_product": 32.0
# }
