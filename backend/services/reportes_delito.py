"""
Servicio para gestión de reportes delictivos
Contiene la lógica de negocio y consultas SQL
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging
from schemas.reporte_delito import ReporteDelitoCreate, ReporteDelitoUpdate


# ========================================
# FUNCIÓN: CREAR REPORTE DELICTIVO
# ========================================
async def crear_reporte_delito(db: AsyncSession, reporte: ReporteDelitoCreate) -> dict:
    """
    Crea un nuevo reporte delictivo en la base de datos.
    
    Args:
        db: Sesión de base de datos asíncrona
        reporte: Datos del reporte a crear (schema Pydantic)
    
    Returns:
        dict: Reporte creado con todos sus datos
    """
    # Query SQL para insertar el nuevo reporte
    query = text("""
        INSERT INTO reportes_delictivos (
            fecha, hora, avenida_id, tipo_delito, nivel_peligrosidad,
            descripcion, usuario_id
        ) VALUES (
            :fecha, :hora, :avenida_id, :tipo_delito, :nivel_peligrosidad,
            :descripcion, :usuario_id
        )
    """)
    
    # Preparar los valores del reporte
    valores = {
        "fecha": reporte.fecha,
        "hora": reporte.hora,
        "avenida_id": reporte.avenida_id,
        "tipo_delito": reporte.tipo_delito,
        "nivel_peligrosidad": reporte.nivel_peligrosidad,
        "descripcion": reporte.descripcion,
        "usuario_id": reporte.usuario_id
    }
    
    # Ejecutar la inserción
    result = await db.execute(query, valores)
    await db.commit()
    
    # Obtener el ID del reporte recién creado
    reporte_id = result.lastrowid
    
    # Devolver el reporte completo
    return await obtener_reporte_delito_por_id(db, reporte_id)


# ========================================
# FUNCIÓN: OBTENER REPORTE POR ID
# ========================================
async def obtener_reporte_delito_por_id(db: AsyncSession, reporte_id: int) -> Optional[dict]:
    """
    Obtiene un reporte delictivo por su ID.
    Incluye información de la avenida y usuario mediante INNER JOIN.
    
    Args:
        db: Sesión de base de datos
        reporte_id: ID del reporte a buscar
    
    Returns:
        dict: Reporte con todos sus datos o None si no existe
    """
    # Query con INNER JOIN para traer información completa
    query = text("""
        SELECT 
            rd.id, rd.fecha, rd.hora, rd.avenida_id, rd.tipo_delito,
            rd.nivel_peligrosidad, rd.descripcion, rd.usuario_id,
            rd.fecha_registro, rd.ultima_modificacion,
            a.nombre as avenida_nombre,
            u.nombre as usuario_nombre
        FROM reportes_delictivos rd
        INNER JOIN avenidas a ON rd.avenida_id = a.id
        INNER JOIN usuarios u ON rd.usuario_id = u.id
        WHERE rd.id = :id
    """)
    
    result = await db.execute(query, {"id": reporte_id})
    reporte = result.fetchone()
    
    if not reporte:
        return None
    
    # Convertir la fila a diccionario
    return {
        "id": reporte.id,
        "fecha": reporte.fecha,
        "hora": reporte.hora,
        "avenida_id": reporte.avenida_id,
        "tipo_delito": reporte.tipo_delito,
        "nivel_peligrosidad": reporte.nivel_peligrosidad,
        "descripcion": reporte.descripcion,
        "usuario_id": reporte.usuario_id,
        "fecha_registro": reporte.fecha_registro,
        "ultima_modificacion": reporte.ultima_modificacion,
        "avenida_nombre": reporte.avenida_nombre,
        "usuario_nombre": reporte.usuario_nombre
    }


# ========================================
# FUNCIÓN: OBTENER TODOS LOS REPORTES
# ========================================
async def obtener_todos_reportes_delito(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    avenida_id: Optional[int] = None,
    tipo_delito: Optional[str] = None,
    nivel_peligrosidad: Optional[str] = None
) -> List[dict]:
    """
    Obtiene lista de reportes delictivos con filtros opcionales.
    Usa INNER JOIN para traer información completa.
    
    Args:
        db: Sesión de base de datos
        skip: Registros a saltar (paginación)
        limit: Máximo de registros a devolver
        avenida_id: Filtrar por avenida (opcional)
        tipo_delito: Filtrar por tipo de delito (opcional)
        nivel_peligrosidad: Filtrar por nivel de peligrosidad (opcional)
    
    Returns:
        List[dict]: Lista de reportes delictivos
    """
    # Construir cláusulas WHERE dinámicamente
    where_clauses = []
    valores = {"skip": skip, "limit": limit}
    
    if avenida_id:
        where_clauses.append("rd.avenida_id = :avenida_id")
        valores["avenida_id"] = avenida_id
    
    if tipo_delito:
        where_clauses.append("rd.tipo_delito = :tipo_delito")
        valores["tipo_delito"] = tipo_delito
    
    if nivel_peligrosidad:
        where_clauses.append("rd.nivel_peligrosidad = :nivel_peligrosidad")
        valores["nivel_peligrosidad"] = nivel_peligrosidad
    
    # Construir el WHERE SQL
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    
    # Query completa con JOINs
    query = text(f"""
        SELECT 
            rd.id, rd.fecha, rd.hora, rd.avenida_id, rd.tipo_delito,
            rd.nivel_peligrosidad, rd.descripcion, rd.usuario_id,
            rd.fecha_registro, rd.ultima_modificacion,
            a.nombre as avenida_nombre,
            u.nombre as usuario_nombre
        FROM reportes_delictivos rd
        INNER JOIN avenidas a ON rd.avenida_id = a.id
        INNER JOIN usuarios u ON rd.usuario_id = u.id
        {where_sql}
        ORDER BY rd.fecha DESC, rd.hora DESC
        LIMIT :limit OFFSET :skip
    """)
    
    result = await db.execute(query, valores)
    reportes = result.fetchall()
    
    # Convertir cada fila a diccionario
    return [
        {
            "id": r.id,
            "fecha": r.fecha,
            "hora": r.hora,
            "avenida_id": r.avenida_id,
            "tipo_delito": r.tipo_delito,
            "nivel_peligrosidad": r.nivel_peligrosidad,
            "descripcion": r.descripcion,
            "usuario_id": r.usuario_id,
            "fecha_registro": r.fecha_registro,
            "ultima_modificacion": r.ultima_modificacion,
            "avenida_nombre": r.avenida_nombre,
            "usuario_nombre": r.usuario_nombre
        }
        for r in reportes
    ]


# ========================================
# FUNCIÓN: ACTUALIZAR REPORTE
# ========================================
async def actualizar_reporte_delito(
    db: AsyncSession, 
    reporte_id: int, 
    reporte_update: ReporteDelitoUpdate
) -> Optional[dict]:
    """
    Actualiza un reporte delictivo existente.
    Solo actualiza los campos que se envían (los demás quedan igual).
    
    Args:
        db: Sesión de base de datos
        reporte_id: ID del reporte a actualizar
        reporte_update: Datos a actualizar
    
    Returns:
        dict: Reporte actualizado o None si no existe
    """
    # Construir dinámicamente los campos a actualizar
    campos_actualizar = []
    valores = {"id": reporte_id}
    
    if reporte_update.fecha is not None:
        campos_actualizar.append("fecha = :fecha")
        valores["fecha"] = reporte_update.fecha
    
    if reporte_update.hora is not None:
        campos_actualizar.append("hora = :hora")
        valores["hora"] = reporte_update.hora
    
    if reporte_update.avenida_id is not None:
        campos_actualizar.append("avenida_id = :avenida_id")
        valores["avenida_id"] = reporte_update.avenida_id
    
    if reporte_update.tipo_delito is not None:
        campos_actualizar.append("tipo_delito = :tipo_delito")
        valores["tipo_delito"] = reporte_update.tipo_delito
    
    if reporte_update.nivel_peligrosidad is not None:
        campos_actualizar.append("nivel_peligrosidad = :nivel_peligrosidad")
        valores["nivel_peligrosidad"] = reporte_update.nivel_peligrosidad
    
    if reporte_update.descripcion is not None:
        campos_actualizar.append("descripcion = :descripcion")
        valores["descripcion"] = reporte_update.descripcion
    
    # Si no hay nada que actualizar, devolver el reporte sin cambios
    if not campos_actualizar:
        return await obtener_reporte_delito_por_id(db, reporte_id)
    
    # Query UPDATE
    query = text(f"""
        UPDATE reportes_delictivos
        SET {', '.join(campos_actualizar)}
        WHERE id = :id
    """)
    
    await db.execute(query, valores)
    await db.commit()
    
    # Devolver el reporte actualizado
    return await obtener_reporte_delito_por_id(db, reporte_id)


# ========================================
# FUNCIÓN: ELIMINAR REPORTE
# ========================================
async def eliminar_reporte_delito(
    db: AsyncSession, 
    reporte_id: int, 
    usuario_id: int, 
    es_admin: bool = False
) -> bool:
    """
    Elimina un reporte delictivo verificando permisos.
    - Admin puede borrar cualquier reporte
    - Usuario normal solo puede borrar sus propios reportes
    
    Args:
        db: Sesión de base de datos
        reporte_id: ID del reporte a eliminar
        usuario_id: ID del usuario que intenta eliminar
        es_admin: Si el usuario es admin
    
    Returns:
        bool: True si se eliminó, False si no existe
    
    Raises:
        PermissionError: Si el usuario no tiene permisos
    """
    try:
        # Verificar si el reporte existe y obtener el usuario creador
        query_verificar = text("""
            SELECT usuario_id FROM reportes_delictivos WHERE id = :reporte_id
        """)
        result = await db.execute(query_verificar, {"reporte_id": reporte_id})
        reporte = result.fetchone()
        
        if not reporte:
            return False
        
        # Verificar permisos
        if not es_admin and reporte.usuario_id != usuario_id:
            raise PermissionError("No tienes permiso para eliminar este reporte")
        
        # Eliminar el reporte
        query_eliminar = text("DELETE FROM reportes_delictivos WHERE id = :reporte_id")
        await db.execute(query_eliminar, {"reporte_id": reporte_id})
        await db.commit()
        
        return True
    
    except PermissionError:
        raise
    except Exception as e:
        await db.rollback()
        logging.error(f"Error al eliminar reporte delictivo {reporte_id}: {str(e)}")
        return False


# ========================================
# FUNCIÓN: CONTAR REPORTES
# ========================================
async def contar_reportes_delito(
    db: AsyncSession,
    avenida_id: Optional[int] = None,
    tipo_delito: Optional[str] = None,
    nivel_peligrosidad: Optional[str] = None
) -> int:
    """
    Cuenta total de reportes delictivos con filtros opcionales.
    Útil para paginación en el frontend.
    
    Args:
        db: Sesión de base de datos
        avenida_id: Filtrar por avenida (opcional)
        tipo_delito: Filtrar por tipo (opcional)
        nivel_peligrosidad: Filtrar por peligrosidad (opcional)
    
    Returns:
        int: Cantidad total de reportes que cumplen los filtros
    """
    where_clauses = []
    valores = {}
    
    if avenida_id:
        where_clauses.append("avenida_id = :avenida_id")
        valores["avenida_id"] = avenida_id
    
    if tipo_delito:
        where_clauses.append("tipo_delito = :tipo_delito")
        valores["tipo_delito"] = tipo_delito
    
    if nivel_peligrosidad:
        where_clauses.append("nivel_peligrosidad = :nivel_peligrosidad")
        valores["nivel_peligrosidad"] = nivel_peligrosidad
    
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    
    query = text(f"""
        SELECT COUNT(*) as total
        FROM reportes_delictivos
        {where_sql}
    """)
    
    result = await db.execute(query, valores)
    row = result.fetchone()
    
    return row.total if row else 0


# ========================================
# NOTAS TÉCNICAS
# ========================================
"""
1. ¿Por qué usar async/await?
   - FastAPI es asíncrono para manejar múltiples requests simultáneas
   - Mejor rendimiento en operaciones I/O (base de datos)
   - No bloquea el servidor mientras espera respuestas de la BD

2. ¿Por qué usar text() en las queries?
   - Es la forma correcta de SQLAlchemy para queries SQL directas
   - Previene inyección SQL al usar parámetros (:variable)
   - Mantiene compatibilidad con async

3. ¿Qué es INNER JOIN?
   - Une dos tablas basándose en una condición
   - Solo devuelve registros que tienen coincidencias en ambas tablas
   - Ejemplo: JOIN avenidas ON rd.avenida_id = a.id

4. ¿Por qué construir WHERE dinámicamente?
   - Permite filtros opcionales (no todos los usuarios usarán todos los filtros)
   - Evita queries complejas con múltiples IF/ELSE
   - Más eficiente y limpio

5. ¿Qué es la paginación (skip/limit)?
   - skip: Cuántos registros saltar (página 1 = 0, página 2 = 100, etc.)
   - limit: Máximo de registros a devolver por página
   - Evita cargar miles de registros de una vez
"""