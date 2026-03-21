"""
Root-level entry point for FastAPI application.
Imports the app from the app package to allow uvicorn to find it easily.
"""

from app.main import app

__all__ = ["app"]
