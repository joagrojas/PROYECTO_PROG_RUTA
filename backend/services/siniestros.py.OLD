"""
Servicio para gestión de siniestros
Incluye consultas complejas con INNER JOIN y subconsultas
"""

from sqlalchemy import text, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging
from schemas.siniestro import SiniestroCreate, SiniestroUpdate

async def crear_siniestro(db: AsyncSession, siniestro: SiniestroCreate) -> dict:
    """Crea un nuevo siniestro"""
    query = text("""
        INSERT INTO siniestros (
            fecha, hora, avenida_id, tipo_id, nivel_gravedad,
            victimas_fatales, heridos, num_vehiculos, dia_semana,
            es_fin_de_semana, usuario_id, observaciones
        ) VALUES (
            :fecha, :hora, :avenida_id, :tipo_id, :nivel_gravedad,
            :victimas_fatales, :heridos, :num_vehiculos, :dia_semana,
            :es_fin_de_semana, :usuario_id, :observaciones
        )
    """)
    
    valores = {
        "fecha": siniestro.fecha,
        "hora": siniestro.hora,
        "avenida_id": siniestro.avenida_id,
        "tipo_id": siniestro.tipo_id,
        "nivel_gravedad": siniestro.nivel_gravedad,
        "victimas_fatales": siniestro.victimas_fatales,
        "heridos": siniestro.heridos,
        "num_vehiculos": siniestro.num_vehiculos,
        "dia_semana": siniestro.dia_semana,
        "es_fin_de_semana": siniestro.es_fin_de_semana,
        "usuario_id": siniestro.usuario_id,
        "observaciones": siniestro.observaciones
    }
    
    result = await db.execute(query, valores)
    await db.commit()
    
    siniestro_id = result.lastrowid
    return await obtener_siniestro_por_id(db, siniestro_id)

async def obtener_siniestro_por_id(db: AsyncSession, siniestro_id: int) -> Optional[dict]:
    """
    Obtiene siniestro por ID con INNER JOIN
    Incluye nombre de avenida, tipo y usuario
    """
    query = text("""
        SELECT 
            s.id, s.fecha, s.hora, s.avenida_id, s.tipo_id,
            s.nivel_gravedad, s.victimas_fatales, s.heridos,
            s.num_vehiculos, s.dia_semana, s.es_fin_de_semana,
            s.usuario_id, s.observaciones, s.fecha_registro,
            s.ultima_modificacion,
            a.nombre as avenida_nombre,
            t.nombre as tipo_nombre,
            u.nombre as usuario_nombre
        FROM siniestros s
        INNER JOIN avenidas a ON s.avenida_id = a.id
        INNER JOIN tipos_siniestro t ON s.tipo_id = t.id
        INNER JOIN usuarios u ON s.usuario_id = u.id
        WHERE s.id = :id
    """)
    
    result = await db.execute(query, {"id": siniestro_id})
    siniestro = result.fetchone()
    
    if not siniestro:
        return None
    
    return {
        "id": siniestro.id,
        "fecha": siniestro.fecha,
        "hora": siniestro.hora,
        "avenida_id": siniestro.avenida_id,
        "tipo_id": siniestro.tipo_id,
        "nivel_gravedad": siniestro.nivel_gravedad,
        "victimas_fatales": siniestro.victimas_fatales,
        "heridos": siniestro.heridos,
        "num_vehiculos": siniestro.num_vehiculos,
        "dia_semana": siniestro.dia_semana,
        "es_fin_de_semana": siniestro.es_fin_de_semana,
        "usuario_id": siniestro.usuario_id,
        "observaciones": siniestro.observaciones,
        "fecha_registro": siniestro.fecha_registro,
        "ultima_modificacion": siniestro.ultima_modificacion,
        "avenida_nombre": siniestro.avenida_nombre,
        "tipo_nombre": siniestro.tipo_nombre,
        "usuario_nombre": siniestro.usuario_nombre
    }

async def obtener_todos_siniestros(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    avenida_id: Optional[int] = None,
    tipo_id: Optional[int] = None,
    nivel_gravedad: Optional[str] = None
) -> List[dict]:
    """
    Obtiene lista de siniestros con filtros opcionales
    Usa INNER JOIN para traer información completa
    """
    where_clauses = []
    valores = {"skip": skip, "limit": limit}
    
    if avenida_id:
        where_clauses.append("s.avenida_id = :avenida_id")
        valores["avenida_id"] = avenida_id
    
    if tipo_id:
        where_clauses.append("s.tipo_id = :tipo_id")
        valores["tipo_id"] = tipo_id
    
    if nivel_gravedad:
        where_clauses.append("s.nivel_gravedad = :nivel_gravedad")
        valores["nivel_gravedad"] = nivel_gravedad
    
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    
    query = text(f"""
        SELECT 
            s.id, s.fecha, s.hora, s.avenida_id, s.tipo_id,
            s.nivel_gravedad, s.victimas_fatales, s.heridos,
            s.num_vehiculos, s.dia_semana, s.es_fin_de_semana,
            s.usuario_id, s.observaciones, s.fecha_registro,
            s.ultima_modificacion,
            a.nombre as avenida_nombre,
            t.nombre as tipo_nombre,
            u.nombre as usuario_nombre
        FROM siniestros s
        INNER JOIN avenidas a ON s.avenida_id = a.id
        INNER JOIN tipos_siniestro t ON s.tipo_id = t.id
        INNER JOIN usuarios u ON s.usuario_id = u.id
        {where_sql}
        ORDER BY s.fecha DESC, s.hora DESC
        LIMIT :limit OFFSET :skip
    """)
    
    result = await db.execute(query, valores)
    siniestros = result.fetchall()
    
    return [
        {
            "id": s.id,
            "fecha": s.fecha,
            "hora": s.hora,
            "avenida_id": s.avenida_id,
            "tipo_id": s.tipo_id,
            "nivel_gravedad": s.nivel_gravedad,
            "victimas_fatales": s.victimas_fatales,
            "heridos": s.heridos,
            "num_vehiculos": s.num_vehiculos,
            "dia_semana": s.dia_semana,
            "es_fin_de_semana": s.es_fin_de_semana,
            "usuario_id": s.usuario_id,
            "observaciones": s.observaciones,
            "fecha_registro": s.fecha_registro,
            "ultima_modificacion": s.ultima_modificacion,
            "avenida_nombre": s.avenida_nombre,
            "tipo_nombre": s.tipo_nombre,
            "usuario_nombre": s.usuario_nombre
        }
        for s in siniestros
    ]

async def actualizar_siniestro(db: AsyncSession, siniestro_id: int, siniestro_update: SiniestroUpdate) -> Optional[dict]:
    """Actualiza siniestro"""
    campos_actualizar = []
    valores = {"id": siniestro_id}
    
    if siniestro_update.fecha is not None:
        campos_actualizar.append("fecha = :fecha")
        valores["fecha"] = siniestro_update.fecha
    
    if siniestro_update.hora is not None:
        campos_actualizar.append("hora = :hora")
        valores["hora"] = siniestro_update.hora
    
    if siniestro_update.avenida_id is not None:
        campos_actualizar.append("avenida_id = :avenida_id")
        valores["avenida_id"] = siniestro_update.avenida_id
    
    if siniestro_update.tipo_id is not None:
        campos_actualizar.append("tipo_id = :tipo_id")
        valores["tipo_id"] = siniestro_update.tipo_id
    
    if siniestro_update.nivel_gravedad is not None:
        campos_actualizar.append("nivel_gravedad = :nivel_gravedad")
        valores["nivel_gravedad"] = siniestro_update.nivel_gravedad
    
    if siniestro_update.victimas_fatales is not None:
        campos_actualizar.append("victimas_fatales = :victimas_fatales")
        valores["victimas_fatales"] = siniestro_update.victimas_fatales
    
    if siniestro_update.heridos is not None:
        campos_actualizar.append("heridos = :heridos")
        valores["heridos"] = siniestro_update.heridos
    
    if siniestro_update.num_vehiculos is not None:
        campos_actualizar.append("num_vehiculos = :num_vehiculos")
        valores["num_vehiculos"] = siniestro_update.num_vehiculos
    
    if siniestro_update.dia_semana is not None:
        campos_actualizar.append("dia_semana = :dia_semana")
        valores["dia_semana"] = siniestro_update.dia_semana
    
    if siniestro_update.es_fin_de_semana is not None:
        campos_actualizar.append("es_fin_de_semana = :es_fin_de_semana")
        valores["es_fin_de_semana"] = siniestro_update.es_fin_de_semana
    
    if siniestro_update.observaciones is not None:
        campos_actualizar.append("observaciones = :observaciones")
        valores["observaciones"] = siniestro_update.observaciones
    
    if not campos_actualizar:
        return await obtener_siniestro_por_id(db, siniestro_id)
    
    query = text(f"""
        UPDATE siniestros
        SET {', '.join(campos_actualizar)}
        WHERE id = :id
    """)
    
    await db.execute(query, valores)
    await db.commit()
    
    return await obtener_siniestro_por_id(db, siniestro_id)

# ✅ CORREGIDO: Función simplificada sin dependencias de modelos
async def eliminar_siniestro(db: AsyncSession, siniestro_id: int, usuario_id: int, es_admin: bool = False) -> bool:
    """
    Elimina un siniestro verificando permisos
    - Admin puede borrar cualquier siniestro
    - Usuario normal solo puede borrar sus propios siniestros
    """
    try:
        # Primero verificar si el siniestro existe y obtener el usuario que lo creó
        query_verificar = text("""
            SELECT usuario_id FROM siniestros WHERE id = :siniestro_id
        """)
        result = await db.execute(query_verificar, {"siniestro_id": siniestro_id})
        siniestro = result.fetchone()
        
        if not siniestro:
            return False
        
        # Verificar permisos
        if not es_admin and siniestro.usuario_id != usuario_id:
            raise PermissionError("No tienes permiso para eliminar este siniestro")
        
        # Eliminar el siniestro
        query_eliminar = text("DELETE FROM siniestros WHERE id = :siniestro_id")
        await db.execute(query_eliminar, {"siniestro_id": siniestro_id})
        await db.commit()
        
        return True

    except PermissionError:
        raise
    except Exception as e:
        await db.rollback()
        logging.error(f"Error al eliminar siniestro {siniestro_id}: {str(e)}")
        return False

async def contar_siniestros(
    db: AsyncSession,
    avenida_id: Optional[int] = None,
    tipo_id: Optional[int] = None,
    nivel_gravedad: Optional[str] = None
) -> int:
    """Cuenta total de siniestros con filtros opcionales"""
    where_clauses = []
    valores = {}
    
    if avenida_id:
        where_clauses.append("avenida_id = :avenida_id")
        valores["avenida_id"] = avenida_id
    
    if tipo_id:
        where_clauses.append("tipo_id = :tipo_id")
        valores["tipo_id"] = tipo_id
    
    if nivel_gravedad:
        where_clauses.append("nivel_gravedad = :nivel_gravedad")
        valores["nivel_gravedad"] = nivel_gravedad
    
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    
    query = text(f"""
        SELECT COUNT(*) as total
        FROM siniestros
        {where_sql}
    """)
    
    result = await db.execute(query, valores)
    row = result.fetchone()
    
    return row.total if row else 0

# ✅ FUNCIÓN ALTERNATIVA: Si prefieres mantener el nombre original pero sin modelos
async def delete_siniestro(db: AsyncSession, siniestro_id: int, usuario_id: int, es_admin: bool = False) -> bool:
    """Alias para eliminar_siniestro - mantiene compatibilidad"""
    return await eliminar_siniestro(db, siniestro_id, usuario_id, es_admin)