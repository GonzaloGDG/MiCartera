"""
Main application for MiCartera API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.cartera import router as cartera_router
from app.routes.cotizaciones import router as cotizaciones_router
from app.routes.liquidez import router as liquidez_router
from app.routes.ahorro import router as ahorro_router
from app.routes.operaciones import router as operaciones_router
from app.routes.tickers import router as tickers_router

tags_metadata = [
    {
        "name": "Autenticación",
        "description": "Gestión de usuarios y login."
    },
    {
        "name": "Cartera",
        "description": "Consulta de la cartera y posiciones."
    },
    {
        "name": "Operaciones",
        "description": "Compras, ventas y dividendos de activos."
    },
    {
        "name": "Ahorro",
        "description": "Movimientos en las cuentas de ahorro."
    },
    {
        "name": "Liquidez",
        "description": "Calculo de la Liquidez."
    },
    {
        "name": "Cotizaciones",
        "description": "Datos de mercado obtenidos de Yahoo Finance."
    },
    {
        "name": "Tickers",
        "description": "Valores."
    }
]

app = FastAPI(
    title="MiCartera API",
    openapi_tags=tags_metadata
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
app.include_router(cartera_router, prefix="/api")
app.include_router(cotizaciones_router, prefix="/api")
app.include_router(liquidez_router, prefix="/api")
app.include_router(ahorro_router, prefix="/api")
app.include_router(operaciones_router, prefix="/api")
app.include_router(tickers_router, prefix="/api")


@app.get("/")
def root():
    return {
        "application": "MiCartera",
        "framework": "FastAPI",
        "status": "OK"
    }