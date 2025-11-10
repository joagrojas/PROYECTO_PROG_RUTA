"""
Servicio para gestión de usuarios
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from services.auth import hashear_password
from datetime import date

async def crear_usuario(db: AsyncSession, usuario: UsuarioCreate) -> dict:
    """Crea un nuevo usuario"""
    password_hash = hashear_password(usuario.password)
    
    query = text("""
        INSERT INTO usuarios (email, password_hash, nombre, rol, fecha_registro, activo)
        VALUES (:email, :password_hash, :nombre, :rol, :fecha_registro, :activo)
    """)
    
    valores = {
        "email": usuario.email,
        "password_hash": password_hash,
        "nombre": usuario.nombre,
        "rol": usuario.rol,
        "fecha_registro": date.today(),
        "activo": True
    }
    
    result = await db.execute(query, valores)
    await db.commit()
    
    # Obtener el usuario creado
    usuario_id = result.lastrowid
    return await obtener_usuario_por_id(db, usuario_id)

async def obtener_usuario_por_id(db: AsyncSession, usuario_id: int) -> Optional[dict]:
    """Obtiene usuario por ID"""
    query = text("""
        SELECT id, email, nombre, rol, fecha_registro, activo, ultimo_acceso
        FROM usuarios
        WHERE id = :id
    """)
    
    result = await db.execute(query, {"id": usuario_id})
    usuario = result.fetchone()
    
    if not usuario:
        return None
    
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "rol": usuario.rol,
        "fecha_registro": usuario.fecha_registro,
        "activo": usuario.activo,
        "ultimo_acceso": usuario.ultimo_acceso
    }

async def obtener_todos_usuarios(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[dict]:
    """Obtiene lista de usuarios con paginación"""
    query = text("""
        SELECT id, email, nombre, rol, fecha_registro, activo, ultimo_acceso
        FROM usuarios
        ORDER BY id DESC
        LIMIT :limit OFFSET :skip
    """)
    
    result = await db.execute(query, {"skip": skip, "limit": limit})
    usuarios = result.fetchall()
    
    return [
        {
            "id": u.id,
            "email": u.email,
            "nombre": u.nombre,
            "rol": u.rol,
            "fecha_registro": u.fecha_registro,
            "activo": u.activo,
            "ultimo_acceso": u.ultimo_acceso
        }
        for u in usuarios
    ]

async def actualizar_usuario(db: AsyncSession, usuario_id: int, usuario_update: UsuarioUpdate) -> Optional[dict]:
    """Actualiza usuario"""
    # Construir query dinámicamente según campos a actualizar
    campos_actualizar = []
    valores = {"id": usuario_id}
    
    if usuario_update.email is not None:
        campos_actualizar.append("email = :email")
        valores["email"] = usuario_update.email
    
    if usuario_update.nombre is not None:
        campos_actualizar.append("nombre = :nombre")
        valores["nombre"] = usuario_update.nombre
    
    if usuario_update.rol is not None:
        campos_actualizar.append("rol = :rol")
        valores["rol"] = usuario_update.rol
    
    if usuario_update.activo is not None:
        campos_actualizar.append("activo = :activo")
        valores["activo"] = usuario_update.activo
    
    if not campos_actualizar:
        return await obtener_usuario_por_id(db, usuario_id)
    
    query = text(f"""
        UPDATE usuarios
        SET {', '.join(campos_actualizar)}
        WHERE id = :id
    """)
    
    await db.execute(query, valores)
    await db.commit()
    
    return await obtener_usuario_por_id(db, usuario_id)

async def eliminar_usuario(db: AsyncSession, usuario_id: int) -> bool:
    """Elimina usuario (soft delete - marca como inactivo)"""
    query = text("""
        UPDATE usuarios
        SET activo = 0
        WHERE id = :id
    """)
    
    result = await db.execute(query, {"id": usuario_id})
    await db.commit()
    
    return result.rowcount > 0