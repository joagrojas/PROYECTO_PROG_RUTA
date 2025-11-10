"""
Router de vehículos involucrados
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from config.database import get_db
from schemas.vehiculo import VehiculoResponse, VehiculoCreate, VehiculoUpdate
from services import vehiculos as vehiculos_service
from routers.auth import obtener_usuario_actual

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

@router.post("/", response_model=VehiculoResponse, status_code=status.HTTP_201_CREATED)
async def crear_vehiculo(
    vehiculo: VehiculoCreate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Crea un nuevo vehículo involucrado"""
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear vehículos"
        )
    return await vehiculos_service.crear_vehiculo(db, vehiculo)

@router.get("/siniestro/{siniestro_id}", response_model=List[VehiculoResponse])
async def listar_vehiculos_por_siniestro(
    siniestro_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """Lista vehículos de un siniestro específico"""
    return await vehiculos_service.obtener_vehiculos_por_siniestro(db, siniestro_id)

@router.get("/{vehiculo_id}", response_model=VehiculoResponse)
async def obtener_vehiculo(
    vehiculo_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """Obtiene un vehículo por ID"""
    vehiculo = await vehiculos_service.obtener_vehiculo_por_id(db, vehiculo_id)
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    return vehiculo

@router.put("/{vehiculo_id}", response_model=VehiculoResponse)
async def actualizar_vehiculo(
    vehiculo_id: int,
    vehiculo_update: VehiculoUpdate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Actualiza un vehículo"""
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar vehículos"
        )
    
    vehiculo = await vehiculos_service.actualizar_vehiculo(db, vehiculo_id, vehiculo_update)
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    return vehiculo

@router.delete("/{vehiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_vehiculo(
    vehiculo_id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Elimina un vehículo"""
    if usuario_actual["rol"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden eliminar vehículos"
        )
    
    eliminado = await vehiculos_service.eliminar_vehiculo(db, vehiculo_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    return None