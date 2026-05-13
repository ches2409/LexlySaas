"""
LEXLY SAAS - FastApi Main Aplication
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv("/media/chesdevos/CHESDEVS1/proyectos/lexlySaas/.env")

# Crear la app

app = FastAPI(
    title="Lexly API",
    description="Saas de gestión jurídica para despachos de extranjeria",
    version="0.1.0"
)

# Configurar CORS (para permitir conexiones desde el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambiar al dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
);

# Importar routers
from backend.app.api import users, health, auth, clientes, casos, caso_documentos, caso_actividades, caso_notas, caso_citas
from backend.app.api.test_db import router as test_db_router
from backend.app.api.debug import router as debug_router


# Incluir routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(clientes.router, prefix="/api/v1", tags=["clientes"])
app.include_router(casos.router, prefix="/api/v1", tags=["casos"])
app.include_router(caso_documentos.router, prefix="/api/v1", tags=["caso-documentos"])
app.include_router(caso_actividades.router, prefix="/api/v1", tags=["caso-actividades"])
app.include_router(caso_notas.router, prefix="/api/v1", tags=["caso-notas"])
app.include_router(caso_citas.router, prefix="/api/v1", tags=["citas"])
app.include_router(test_db_router, prefix="/api/v1", tags=["debug"])
app.include_router(debug_router, prefix="/api/v1", tags=["debug"])

