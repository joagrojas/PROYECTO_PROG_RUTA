"""
Sistema de Gestión de Siniestros Viales - La Rioja
FastAPI Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config.settings import settings
from config.database import init_db, close_db

# Importar routers
from routers import (
    auth_router,
    usuarios_router,
    avenidas_router,
    tipos_siniestro_router,
    siniestros_router,
    vehiculos_router,
    reportes_router
)

# Lifecycle events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo de eventos de inicio y cierre de la aplicación"""
    # Startup
    await init_db()
    print("✅ Base de datos inicializada")
    yield
    # Shutdown
    await close_db()
    print("✅ Conexiones cerradas")

# Crear aplicación
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan
)

# logging básico para ver tracebacks en la consola
logging.basicConfig(level=logging.INFO)

# CORS: permitir el front durante desarrollo
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(avenidas_router)
app.include_router(tipos_siniestro_router)
app.include_router(siniestros_router)
app.include_router(vehiculos_router)
app.include_router(reportes_router)

# Ruta raíz
@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "mensaje": "Sistema de Gestión de Siniestros Viales - API",
        "version": settings.API_VERSION,
        "documentacion": "/docs",
        "status": "activo"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )