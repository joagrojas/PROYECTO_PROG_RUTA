"""
Schemas para autenticación y JWT
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema para datos decodificados del token"""
    email: Optional[str] = None
    rol: Optional[str] = None

class LoginRequest(BaseModel):
    """Schema para solicitud de login"""
    email: EmailStr
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "admin@transitolarioja.gob.ar",
                    "password": "admin123"
                }
            ]
        }
    }

class RegisterRequest(BaseModel):
    """Schema para registro de nuevo usuario"""
    email: EmailStr
    password: str
    nombre: str
    rol: str = "consultor"
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "nuevo@transitolarioja.gob.ar",
                    "password": "password123",
                    "nombre": "Juan Pérez",
                    "rol": "editor"
                }
            ]
        }
    }

class ChangePasswordRequest(BaseModel):
    """Schema para cambio de contraseña"""
    old_password: str
    new_password: str