"""
Main application for MiCartera API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router

app = FastAPI(
    title="MiCartera API",
    version="1.0.0"
)

# CORS para permitir llamadas desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Más adelante lo restringiremos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")


@app.get("/")
def root():
    return {
        "application": "MiCartera",
        "framework": "FastAPI",
        "status": "OK"
    }