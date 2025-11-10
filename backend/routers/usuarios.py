"""
Router de usuarios
Endpoints CRUD para usuarios
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from config.database import get_db
from schemas.usuario import UsuarioResponse, UsuarioCreate, UsuarioUpdate
from services import usuarios as usuarios_service
from routers.auth import obtener_usuario_actual

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def verificar_admin(usuario_actual: dict = Depends(obtener_usuario_actual)):
    """Verifica que el usuario sea admin"""
    if usuario_actual["rol"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    return usuario_actual

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(verificar_admin)
):
    """Crea un nuevo usuario (solo admin)"""
    return await usuarios_service.crear_usuario(db, usuario)

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """Lista todos los usuarios"""
    return await usuarios_service.obtener_todos_usuarios(db, skip, limit)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(obtener_usuario_actual)
):
    """Obtiene un usuario por ID"""
    usuario = await usuarios_service.obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(verificar_admin)
):
    """Actualiza un usuario (solo admin)"""
    usuario = await usuarios_service.actualizar_usuario(db, usuario_id, usuario_update)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(verificar_admin)
):
    """Elimina un usuario (solo admin)"""
    eliminado = await usuarios_service.eliminar_usuario(db, usuario_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return None