"""
Router de siniestros
Endpoints CRUD para siniestros
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from config.database import get_db
from schemas.siniestro import SiniestroCreate, SiniestroUpdate, SiniestroOut, SiniestroResponse
from services import siniestros as siniestros_service
from services.auth import obtener_usuario_actual

router = APIRouter(prefix="/siniestros", tags=["Siniestros"])


# ========================================
# FUNCIONES AUXILIARES
# ========================================
def _sanitize_row(row: dict) -> dict:
    """Normaliza valores inconsistentes en los registros devueltos"""
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
# ENDPOINTS
# ========================================

@router.post("/", response_model=SiniestroResponse, status_code=status.HTTP_201_CREATED)
async def crear_siniestro(
    siniestro: SiniestroCreate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Crea un nuevo siniestro"""
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear siniestros"
        )
    return await siniestros_service.crear_siniestro(db, siniestro)


@router.get("/", response_model=List[SiniestroOut])
async def listar_siniestros(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    avenida_id: Optional[int] = None,
    tipo_id: Optional[int] = None,
    nivel_gravedad: Optional[str] = None,
    db = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """Lista siniestros con filtros opcionales"""
    raw = await siniestros_service.obtener_todos_siniestros(
        db, skip, limit, avenida_id, tipo_id, nivel_gravedad
    )
    items = jsonable_encoder(raw)
    items_saneados = [_sanitize_row(i) for i in items]
    return JSONResponse(content=items_saneados)


@router.get("/count")
async def contar_siniestros(
    avenida_id: Optional[int] = None,
    tipo_id: Optional[int] = None,
    nivel_gravedad: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """Cuenta total de siniestros con filtros"""
    total = await siniestros_service.contar_siniestros(
        db, avenida_id, tipo_id, nivel_gravedad
    )
    return {"total": total}


@router.get("/{siniestro_id}", response_model=SiniestroResponse)
async def obtener_siniestro(
    siniestro_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """Obtiene un siniestro por ID"""
    siniestro = await siniestros_service.obtener_siniestro_por_id(db, siniestro_id)
    if not siniestro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Siniestro no encontrado"
        )
    return siniestro


@router.put("/{siniestro_id}", response_model=SiniestroResponse)
async def actualizar_siniestro(
    siniestro_id: int,
    siniestro_update: SiniestroUpdate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Actualiza un siniestro"""
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar siniestros"
        )
    
    siniestro = await siniestros_service.actualizar_siniestro(
        db, siniestro_id, siniestro_update
    )
    if not siniestro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Siniestro no encontrado"
        )
    return siniestro


@router.delete("/{siniestro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_siniestro(
    siniestro_id: int,
    db: AsyncSession = Depends(get_db),
    usuario: dict = Depends(obtener_usuario_actual)
):
    """Elimina un siniestro"""
    try:
        # ✅ CORREGIDO: Extraer los datos necesarios del usuario
        usuario_id = usuario.get("id")
        es_admin = usuario.get("rol") == "admin"  # Basado en tu estructura de usuario
        
        if not usuario_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado correctamente"
            )
        
        success = await siniestros_service.eliminar_siniestro(
            db=db,
            siniestro_id=siniestro_id,
            usuario_id=usuario_id,
            es_admin=es_admin
        )
        
        if success:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Siniestro no encontrado"
            )
            
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception:
        logging.exception("Error al eliminar siniestro %s", siniestro_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al eliminar siniestro"
        )
