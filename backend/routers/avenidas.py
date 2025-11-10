"""
Router de avenidas
Endpoints CRUD para avenidas
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from config.database import get_db
from schemas.avenida import AvenidaResponse, AvenidaCreate, AvenidaUpdate
from services import avenidas as avenidas_service
from routers.auth import obtener_usuario_actual

router = APIRouter(prefix="/avenidas", tags=["Avenidas"])

@router.post("/", response_model=AvenidaResponse, status_code=status.HTTP_201_CREATED)
async def crear_avenida(
    avenida: AvenidaCreate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Crea una nueva avenida"""
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear avenidas"
        )
    return await avenidas_service.crear_avenida(db, avenida)

@router.get("/", response_model=List[AvenidaResponse])
async def listar_avenidas(
    db: AsyncSession = Depends(get_db)
):
    """Lista todas las avenidas (público)"""
    return await avenidas_service.obtener_todas_avenidas(db)

@router.get("/{avenida_id}", response_model=AvenidaResponse)
async def obtener_avenida(
    avenida_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene una avenida por ID"""
    avenida = await avenidas_service.obtener_avenida_por_id(db, avenida_id)
    if not avenida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avenida no encontrada"
        )
    return avenida

@router.put("/{avenida_id}", response_model=AvenidaResponse)
async def actualizar_avenida(
    avenida_id: int,
    avenida_update: AvenidaUpdate,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Actualiza una avenida"""
    if usuario_actual["rol"] not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar avenidas"
        )
    
    avenida = await avenidas_service.actualizar_avenida(db, avenida_id, avenida_update)
    if not avenida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avenida no encontrada"
        )
    return avenida

@router.delete("/{avenida_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_avenida(
    avenida_id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """Elimina una avenida"""
    if usuario_actual["rol"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden eliminar avenidas"
        )
    
    eliminado = await avenidas_service.eliminar_avenida(db, avenida_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avenida no encontrada"
        )
    return None