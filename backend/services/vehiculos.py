"""
Servicio para gestión de vehículos involucrados
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from schemas.vehiculo import VehiculoCreate, VehiculoUpdate

async def crear_vehiculo(db: AsyncSession, vehiculo: VehiculoCreate) -> dict:
    """Crea un nuevo vehículo involucrado"""
    query = text("""
        INSERT INTO vehiculos_involucrados (
            siniestro_id, tipo_vehiculo, marca, modelo, rol, es_fallecido
        ) VALUES (
            :siniestro_id, :tipo_vehiculo, :marca, :modelo, :rol, :es_fallecido
        )
    """)
    
    valores = {
        "siniestro_id": vehiculo.siniestro_id,
        "tipo_vehiculo": vehiculo.tipo_vehiculo,
        "marca": vehiculo.marca,
        "modelo": vehiculo.modelo,
        "rol": vehiculo.rol,
        "es_fallecido": vehiculo.es_fallecido
    }
    
    result = await db.execute(query, valores)
    await db.commit()
    
    vehiculo_id = result.lastrowid
    return await obtener_vehiculo_por_id(db, vehiculo_id)

async def obtener_vehiculo_por_id(db: AsyncSession, vehiculo_id: int) -> Optional[dict]:
    """Obtiene vehículo por ID"""
    query = text("""
        SELECT vehiculo_id, siniestro_id, tipo_vehiculo, marca, modelo, rol, es_fallecido
        FROM vehiculos_involucrados
        WHERE vehiculo_id = :id
    """)
    
    result = await db.execute(query, {"id": vehiculo_id})
    vehiculo = result.fetchone()
    
    if not vehiculo:
        return None
    
    return {
        "vehiculo_id": vehiculo.vehiculo_id,
        "siniestro_id": vehiculo.siniestro_id,
        "tipo_vehiculo": vehiculo.tipo_vehiculo,
        "marca": vehiculo.marca,
        "modelo": vehiculo.modelo,
        "rol": vehiculo.rol,
        "es_fallecido": vehiculo.es_fallecido
    }

async def obtener_vehiculos_por_siniestro(db: AsyncSession, siniestro_id: int) -> List[dict]:
    """Obtiene todos los vehículos de un siniestro específico"""
    query = text("""
        SELECT vehiculo_id, siniestro_id, tipo_vehiculo, marca, modelo, rol, es_fallecido
        FROM vehiculos_involucrados
        WHERE siniestro_id = :siniestro_id
        ORDER BY vehiculo_id
    """)
    
    result = await db.execute(query, {"siniestro_id": siniestro_id})
    vehiculos = result.fetchall()
    
    return [
        {
            "vehiculo_id": v.vehiculo_id,
            "siniestro_id": v.siniestro_id,
            "tipo_vehiculo": v.tipo_vehiculo,
            "marca": v.marca,
            "modelo": v.modelo,
            "rol": v.rol,
            "es_fallecido": v.es_fallecido
        }
        for v in vehiculos
    ]

async def actualizar_vehiculo(db: AsyncSession, vehiculo_id: int, vehiculo_update: VehiculoUpdate) -> Optional[dict]:
    """Actualiza vehículo"""
    campos_actualizar = []
    valores = {"id": vehiculo_id}
    
    if vehiculo_update.tipo_vehiculo is not None:
        campos_actualizar.append("tipo_vehiculo = :tipo_vehiculo")
        valores["tipo_vehiculo"] = vehiculo_update.tipo_vehiculo
    
    if vehiculo_update.marca is not None:
        campos_actualizar.append("marca = :marca")
        valores["marca"] = vehiculo_update.marca
    
    if vehiculo_update.modelo is not None:
        campos_actualizar.append("modelo = :modelo")
        valores["modelo"] = vehiculo_update.modelo
    
    if vehiculo_update.rol is not None:
        campos_actualizar.append("rol = :rol")
        valores["rol"] = vehiculo_update.rol
    
    if vehiculo_update.es_fallecido is not None:
        campos_actualizar.append("es_fallecido = :es_fallecido")
        valores["es_fallecido"] = vehiculo_update.es_fallecido
    
    if not campos_actualizar:
        return await obtener_vehiculo_por_id(db, vehiculo_id)
    
    query = text(f"""
        UPDATE vehiculos_involucrados
        SET {', '.join(campos_actualizar)}
        WHERE vehiculo_id = :id
    """)
    
    await db.execute(query, valores)
    await db.commit()
    
    return await obtener_vehiculo_por_id(db, vehiculo_id)

async def eliminar_vehiculo(db: AsyncSession, vehiculo_id: int) -> bool:
    """Elimina vehículo"""
    query = text("""
        DELETE FROM vehiculos_involucrados
        WHERE vehiculo_id = :id
    """)
    
    result = await db.execute(query, {"id": vehiculo_id})
    await db.commit()
    
    return result.rowcount > 0