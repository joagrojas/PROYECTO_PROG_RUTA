"""
Servicio para gestión de avenidas
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from schemas.avenida import AvenidaCreate, AvenidaUpdate

async def crear_avenida(db: AsyncSession, avenida: AvenidaCreate) -> dict:
    """Crea una nueva avenida"""
    query = text("""
        INSERT INTO avenidas (nombre, tipo, zona, longitud_km)
        VALUES (:nombre, :tipo, :zona, :longitud_km)
    """)
    
    valores = {
        "nombre": avenida.nombre,
        "tipo": avenida.tipo,
        "zona": avenida.zona,
        "longitud_km": avenida.longitud_km
    }
    
    result = await db.execute(query, valores)
    await db.commit()
    
    avenida_id = result.lastrowid
    return await obtener_avenida_por_id(db, avenida_id)

async def obtener_avenida_por_id(db: AsyncSession, avenida_id: int) -> Optional[dict]:
    """Obtiene avenida por ID"""
    query = text("""
        SELECT id, nombre, tipo, zona, longitud_km
        FROM avenidas
        WHERE id = :id
    """)
    
    result = await db.execute(query, {"id": avenida_id})
    avenida = result.fetchone()
    
    if not avenida:
        return None
    
    return {
        "id": avenida.id,
        "nombre": avenida.nombre,
        "tipo": avenida.tipo,
        "zona": avenida.zona,
        "longitud_km": avenida.longitud_km
    }

async def obtener_todas_avenidas(db: AsyncSession) -> List[dict]:
    """Obtiene todas las avenidas"""
    query = text("""
        SELECT id, nombre, tipo, zona, longitud_km
        FROM avenidas
        ORDER BY nombre
    """)
    
    result = await db.execute(query)
    avenidas = result.fetchall()
    
    return [
        {
            "id": a.id,
            "nombre": a.nombre,
            "tipo": a.tipo,
            "zona": a.zona,
            "longitud_km": a.longitud_km
        }
        for a in avenidas
    ]

async def actualizar_avenida(db: AsyncSession, avenida_id: int, avenida_update: AvenidaUpdate) -> Optional[dict]:
    """Actualiza avenida"""
    campos_actualizar = []
    valores = {"id": avenida_id}
    
    if avenida_update.nombre is not None:
        campos_actualizar.append("nombre = :nombre")
        valores["nombre"] = avenida_update.nombre
    
    if avenida_update.tipo is not None:
        campos_actualizar.append("tipo = :tipo")
        valores["tipo"] = avenida_update.tipo
    
    if avenida_update.zona is not None:
        campos_actualizar.append("zona = :zona")
        valores["zona"] = avenida_update.zona
    
    if avenida_update.longitud_km is not None:
        campos_actualizar.append("longitud_km = :longitud_km")
        valores["longitud_km"] = avenida_update.longitud_km
    
    if not campos_actualizar:
        return await obtener_avenida_por_id(db, avenida_id)
    
    query = text(f"""
        UPDATE avenidas
        SET {', '.join(campos_actualizar)}
        WHERE id = :id
    """)
    
    await db.execute(query, valores)
    await db.commit()
    
    return await obtener_avenida_por_id(db, avenida_id)

async def eliminar_avenida(db: AsyncSession, avenida_id: int) -> bool:
    """Elimina avenida"""
    query = text("""
        DELETE FROM avenidas
        WHERE id = :id
    """)
    
    result = await db.execute(query, {"id": avenida_id})
    await db.commit()
    
    return result.rowcount > 0