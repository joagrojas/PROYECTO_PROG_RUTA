"""
Configuración de conexión a base de datos MySQL
Usando SQLAlchemy con soporte asíncrono
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text  # ← IMPORTANTE: Importar text
from typing import AsyncGenerator
from .settings import settings

# URL de conexión asíncrona a MySQL
DATABASE_URL = f"mysql+aiomysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# Motor asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Cambiado a False para no ver tanto log
    pool_pre_ping=True,
    pool_recycle=3600
)

# Session maker asíncrono
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base para modelos (si los necesitas)
Base = declarative_base()

# Dependency para FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency que provee una sesión de base de datos
    Se cierra automáticamente después de cada request
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Funciones de inicialización y cierre
async def init_db():
    """Inicializa la conexión a la base de datos"""
    try:
        async with engine.begin() as conn:
            # Verificar conexión - USAR text()
            await conn.execute(text("SELECT 1"))
        print("✅ Conexión a MySQL establecida exitosamente")
    except Exception as e:
        print(f"❌ Error al conectar con MySQL: {e}")
        raise

async def close_db():
    """Cierra todas las conexiones a la base de datos"""
    await engine.dispose()
    print("✅ Conexiones a MySQL cerradas")