"""
Router de tipos de siniestro
Endpoints CRUD para tipos de siniestro
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from config.database import get_db
from schemas.tipo_siniestro import TipoSiniestroResponse, TipoSiniestroCreate, TipoSiniestroUpdate
from services import tipos_siniestro as tipos_service
from routers.auth import obtener_usuario_actual

router = APIRouter(prefix="/tipos-siniestro", tags=["Tipos de Siniestro"])

@router.post("/", response_model=TipoSiniestroResponse, status_code=status.HTTP_201_CREATED)
async def crear_tipo_siniestro(
    tipo: TipoSiniestroCreate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Crea un nuevo tipo de siniestro"""
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear tipos de siniestro"
        )
    return await tipos_service.crear_tipo_siniestro(db, tipo)

@router.get("/", response_model=List[TipoSiniestroResponse])
async def listar_tipos_siniestro(
    db: AsyncSession = Depends(get_db)
):
    """Lista todos los tipos de siniestro (público)"""
    return await tipos_service.obtener_todos_tipos_siniestro(db)

@router.get("/{tipo_id}", response_model=TipoSiniestroResponse)
async def obtener_tipo_siniestro(
    tipo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene un tipo de siniestro por ID"""
    tipo = await tipos_service.obtener_tipo_siniestro_por_id(db, tipo_id)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de siniestro no encontrado"
        )
    return tipo

@router.put("/{tipo_id}", response_model=TipoSiniestroResponse)
async def actualizar_tipo_siniestro(
    tipo_id: int,
    tipo_update: TipoSiniestroUpdate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Actualiza un tipo de siniestro"""
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar tipos"
        )
    
    tipo = await tipos_service.actualizar_tipo_siniestro(db, tipo_id, tipo_update)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de siniestro no encontrado"
        )
    return tipo

@router.delete("/{tipo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_tipo_siniestro(
    tipo_id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Elimina un tipo de siniestro"""
    if usuario_actual["rol"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden eliminar tipos"
        )
    
    eliminado = await tipos_service.eliminar_tipo_siniestro(db, tipo_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de siniestro no encontrado"
        )
    return None