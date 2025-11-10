"""
Router de reportes delictivos
Endpoints CRUD para gestión de reportes de delitos
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from config.database import get_db
from schemas.reporte_delito import (
    ReporteDelitoCreate, 
    ReporteDelitoUpdate, 
    ReporteDelitoOut, 
    ReporteDelitoResponse
)
from services import reportes_delito as reportes_delito_service
from services.auth import obtener_usuario_actual

# Crear router con prefijo y tag
router = APIRouter(prefix="/reportes-delito", tags=["Reportes Delictivos"])


# ========================================
# FUNCIONES AUXILIARES
# ========================================
def _sanitize_row(row: dict) -> dict:
    """
    Normaliza valores inconsistentes en los registros devueltos.
    Maneja conversión de timedelta a string para hora.
    """
    r = dict(row)
    
    # Normalizar fecha inválida '0000-00-00' -> None
    fecha = r.get("fecha")
    if isinstance(fecha, str) and fecha.strip() in ("", "0000-00-00"):
        r["fecha"] = None
    
    # Normalizar hora (timedelta -> "HH:MM:SS")
    hora = r.get("hora")
    if isinstance(hora, timedelta):
        total = int(hora.total_seconds())
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        r["hora"] = f"{hh:02d}:{mm:02d}:{ss:02d}"
    
    # Si hora es número/otro formato, convertir a string seguro
    if r.get("hora") is not None and not isinstance(r.get("hora"), str):
        r["hora"] = str(r["hora"])
    
    return r


# ========================================
# ENDPOINTS CRUD
# ========================================

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_reporte_delito(
    reporte: ReporteDelitoCreate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """
    Crea un nuevo reporte delictivo.
    
    Requiere rol: admin o editor
    
    Args:
        reporte: Datos del reporte a crear
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado
    
    Returns:
        JSONResponse: Reporte creado con mensaje de éxito
    
    Raises:
        HTTPException 403: Si el usuario no tiene permisos
    """
    # Verificar permisos
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear reportes delictivos"
        )
    
    # Crear el reporte
    nuevo_reporte = await reportes_delito_service.crear_reporte_delito(db, reporte)
    
    # Sanitizar la respuesta (convierte timedelta a string)
    reporte_sanitizado = _sanitize_row(nuevo_reporte)
    
    # Convertir a JSON serializable (date, datetime, etc.)
    reporte_json = jsonable_encoder(reporte_sanitizado)
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "mensaje": "Reporte delictivo creado exitosamente",
            "reporte": reporte_json
        }
    )


@router.get("/", response_model=List[ReporteDelitoOut])
async def listar_reportes_delito(
    skip: int = Query(0, ge=0, description="Registros a saltar (paginación)"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    avenida_id: Optional[int] = Query(None, description="Filtrar por ID de avenida"),
    tipo_delito: Optional[str] = Query(None, description="Filtrar por tipo de delito"),
    nivel_peligrosidad: Optional[str] = Query(None, description="Filtrar por nivel de peligrosidad"),
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """
    Lista reportes delictivos con filtros opcionales.
    
    Parámetros de consulta:
        - skip: Cuántos registros saltar (default: 0)
        - limit: Máximo de registros (default: 100, max: 1000)
        - avenida_id: Filtrar por avenida específica
        - tipo_delito: Filtrar por tipo (robo, asalto, hurto, vandalismo, otro)
        - nivel_peligrosidad: Filtrar por nivel (baja, media, alta)
    
    Returns:
        List[ReporteDelitoOut]: Lista de reportes delictivos
    """
    # Obtener reportes del servicio
    reportes = await reportes_delito_service.obtener_todos_reportes_delito(
        db, skip, limit, avenida_id, tipo_delito, nivel_peligrosidad
    )
    
    # Convertir a JSON y sanitizar
    items = jsonable_encoder(reportes)
    items_saneados = [_sanitize_row(i) for i in items]
    
    return JSONResponse(content=items_saneados)


@router.get("/count")
async def contar_reportes_delito(
    avenida_id: Optional[int] = Query(None, description="Filtrar por avenida"),
    tipo_delito: Optional[str] = Query(None, description="Filtrar por tipo"),
    nivel_peligrosidad: Optional[str] = Query(None, description="Filtrar por peligrosidad"),
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """
    Cuenta total de reportes delictivos con filtros opcionales.
    Útil para paginación en el frontend.
    
    Returns:
        dict: {"total": número_de_reportes}
    """
    total = await reportes_delito_service.contar_reportes_delito(
        db, avenida_id, tipo_delito, nivel_peligrosidad
    )
    return {"total": total}


@router.get("/{reporte_id}")
async def obtener_reporte_delito(
    reporte_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """
    Obtiene un reporte delictivo por su ID.
    
    Args:
        reporte_id: ID del reporte a buscar
    
    Returns:
        JSONResponse: Reporte encontrado con mensaje
    
    Raises:
        HTTPException 404: Si el reporte no existe
    """
    reporte = await reportes_delito_service.obtener_reporte_delito_por_id(db, reporte_id)
    
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte delictivo no encontrado"
        )
    
    # Sanitizar y convertir a JSON serializable
    reporte_sanitizado = _sanitize_row(reporte)
    reporte_json = jsonable_encoder(reporte_sanitizado)
    
    return JSONResponse(content={
        "mensaje": "Reporte delictivo obtenido exitosamente",
        "reporte": reporte_json
    })


@router.put("/{reporte_id}")
async def actualizar_reporte_delito(
    reporte_id: int,
    reporte_update: ReporteDelitoUpdate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """
    Actualiza un reporte delictivo existente.
    
    Requiere rol: admin o editor
    
    Args:
        reporte_id: ID del reporte a actualizar
        reporte_update: Campos a actualizar
    
    Returns:
        JSONResponse: Reporte actualizado con mensaje
    
    Raises:
        HTTPException 403: Si no tiene permisos
        HTTPException 404: Si el reporte no existe
    """
    # Verificar permisos
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar reportes delictivos"
        )
    
    # Actualizar reporte
    reporte = await reportes_delito_service.actualizar_reporte_delito(
        db, reporte_id, reporte_update
    )
    
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte delictivo no encontrado"
        )
    
    # Sanitizar y convertir a JSON serializable
    reporte_sanitizado = _sanitize_row(reporte)
    reporte_json = jsonable_encoder(reporte_sanitizado)
    
    return JSONResponse(content={
        "mensaje": "Reporte delictivo actualizado exitosamente",
        "reporte": reporte_json
    })


@router.delete("/{reporte_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_reporte_delito(
    reporte_id: int,
    db: AsyncSession = Depends(get_db),
    usuario: dict = Depends(obtener_usuario_actual)
):
    """
    Elimina un reporte delictivo.
    
    Permisos:
        - Admin: Puede eliminar cualquier reporte
        - Editor: Solo puede eliminar sus propios reportes
        - Consultor: No puede eliminar
    
    Args:
        reporte_id: ID del reporte a eliminar
    
    Returns:
        204 No Content si se eliminó exitosamente
    
    Raises:
        HTTPException 403: Si no tiene permisos
        HTTPException 404: Si el reporte no existe
        HTTPException 500: Error interno
    """
    try:
        # Extraer datos del usuario
        usuario_id = usuario.get("id")
        es_admin = usuario.get("rol") == "admin"
        
        if not usuario_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado correctamente"
            )
        
        # Intentar eliminar
        success = await reportes_delito_service.eliminar_reporte_delito(
            db=db,
            reporte_id=reporte_id,
            usuario_id=usuario_id,
            es_admin=es_admin
        )
        
        if success:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reporte delictivo no encontrado"
            )
    
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Error al eliminar reporte delictivo %s", reporte_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al eliminar reporte delictivo"
        )


# ========================================
# NOTAS TÉCNICAS
# ========================================
"""
CORRECCIONES APLICADAS:

1. Sanitización de campo 'hora':
   - Convierte timedelta a string "HH:MM:SS"
   - Aplicado a todos los endpoints que devuelven reportes

2. Serialización JSON:
   - Usa jsonable_encoder() para convertir objetos Python (date, datetime) a JSON
   - Aplicado DESPUÉS de sanitizar
   - Necesario porque JSONResponse requiere tipos JSON nativos

FLUJO CORRECTO:
1. Obtener datos de la BD → (puede incluir date, datetime, timedelta)
2. Sanitizar con _sanitize_row() → (convierte timedelta a string)
3. Convertir con jsonable_encoder() → (convierte date/datetime a string ISO)
4. Devolver con JSONResponse → ✅ Todo es JSON serializable

CONCEPTOS:
- timedelta: Diferencia de tiempo (ej: 14 horas, 30 minutos)
- date: Fecha sin hora (ej: 2025-11-10)
- datetime: Fecha y hora (ej: 2025-11-10T15:30:00)
- JSON solo acepta: string, number, boolean, array, object, null
"""