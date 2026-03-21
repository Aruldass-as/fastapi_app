from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS

def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Authorization"],
    )
