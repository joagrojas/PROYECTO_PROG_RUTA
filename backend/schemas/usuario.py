"""
Schemas para Usuario
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class UsuarioBase(BaseModel):
    """Schema base de usuario"""
    email: EmailStr
    nombre: str
    rol: str

class UsuarioCreate(UsuarioBase):
    """Schema para crear usuario"""
    password: str

class UsuarioUpdate(BaseModel):
    """Schema para actualizar usuario"""
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    """Schema para respuesta de usuario (sin password)"""
    id: int
    fecha_registro: date
    activo: bool
    ultimo_acceso: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class UsuarioInDB(UsuarioResponse):
    """Schema de usuario en base de datos (con password hash)"""
    password_hash: str