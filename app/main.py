"""
LEXLY SAAS - FastAPI Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear la app
app = FastAPI(
    title="Lexly API",
    description="SaaS de gestión jurídica para despachos de extranjería",
    version="0.1.0"
)

# Configurar CORS (para permitir conexiones desde el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar routers
from app.api import users, health

# Incluir routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])