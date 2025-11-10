"""
Servicio para gestión de tipos de siniestro
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from schemas.tipo_siniestro import TipoSiniestroCreate, TipoSiniestroUpdate

async def crear_tipo_siniestro(db: AsyncSession, tipo: TipoSiniestroCreate) -> dict:
    """Crea un nuevo tipo de siniestro"""
    query = text("""
        INSERT INTO tipos_siniestro (nombre, gravedad, descripcion)
        VALUES (:nombre, :gravedad, :descripcion)
    """)
    
    valores = {
        "nombre": tipo.nombre,
        "gravedad": tipo.gravedad,
        "descripcion": tipo.descripcion
    }
    
    result = await db.execute(query, valores)
    await db.commit()
    
    tipo_id = result.lastrowid
    return await obtener_tipo_siniestro_por_id(db, tipo_id)

async def obtener_tipo_siniestro_por_id(db: AsyncSession, tipo_id: int) -> Optional[dict]:
    """Obtiene tipo de siniestro por ID"""
    query = text("""
        SELECT id, nombre, gravedad, descripcion
        FROM tipos_siniestro
        WHERE id = :id
    """)
    
    result = await db.execute(query, {"id": tipo_id})
    tipo = result.fetchone()
    
    if not tipo:
        return None
    
    return {
        "id": tipo.id,
        "nombre": tipo.nombre,
        "gravedad": tipo.gravedad,
        "descripcion": tipo.descripcion
    }

async def obtener_todos_tipos_siniestro(db: AsyncSession) -> List[dict]:
    """Obtiene todos los tipos de siniestro"""
    query = text("""
        SELECT id, nombre, gravedad, descripcion
        FROM tipos_siniestro
        ORDER BY gravedad DESC, nombre
    """)
    
    result = await db.execute(query)
    tipos = result.fetchall()
    
    return [
        {
            "id": t.id,
            "nombre": t.nombre,
            "gravedad": t.gravedad,
            "descripcion": t.descripcion
        }
        for t in tipos
    ]

async def actualizar_tipo_siniestro(db: AsyncSession, tipo_id: int, tipo_update: TipoSiniestroUpdate) -> Optional[dict]:
    """Actualiza tipo de siniestro"""
    campos_actualizar = []
    valores = {"id": tipo_id}
    
    if tipo_update.nombre is not None:
        campos_actualizar.append("nombre = :nombre")
        valores["nombre"] = tipo_update.nombre
    
    if tipo_update.gravedad is not None:
        campos_actualizar.append("gravedad = :gravedad")
        valores["gravedad"] = tipo_update.gravedad
    
    if tipo_update.descripcion is not None:
        campos_actualizar.append("descripcion = :descripcion")
        valores["descripcion"] = tipo_update.descripcion
    
    if not campos_actualizar:
        return await obtener_tipo_siniestro_por_id(db, tipo_id)
    
    query = text(f"""
        UPDATE tipos_siniestro
        SET {', '.join(campos_actualizar)}
        WHERE id = :id
    """)
    
    await db.execute(query, valores)
    await db.commit()
    
    return await obtener_tipo_siniestro_por_id(db, tipo_id)

async def eliminar_tipo_siniestro(db: AsyncSession, tipo_id: int) -> bool:
    """Elimina tipo de siniestro"""
    query = text("""
        DELETE FROM tipos_siniestro
        WHERE id = :id
    """)
    
    result = await db.execute(query, {"id": tipo_id})
    await db.commit()
    
    return result.rowcount > 0