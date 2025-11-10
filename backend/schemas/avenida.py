"""
Schemas para Avenida
"""

from pydantic import BaseModel, Field
from typing import Optional

class AvenidaBase(BaseModel):
    """Schema base de avenida"""
    nombre: str = Field(..., min_length=1, max_length=100)
    tipo: str = Field(..., pattern="^(avenida|ruta|calle)$")
    zona: str = Field(..., min_length=1, max_length=50)
    longitud_km: float = Field(..., gt=0)

class AvenidaCreate(AvenidaBase):
    """Schema para crear avenida"""
    pass

class AvenidaUpdate(BaseModel):
    """Schema para actualizar avenida"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo: Optional[str] = Field(None, pattern="^(avenida|ruta|calle)$")
    zona: Optional[str] = Field(None, min_length=1, max_length=50)
    longitud_km: Optional[float] = Field(None, gt=0)

class AvenidaResponse(AvenidaBase):
    """Schema para respuesta de avenida"""
    id: int
    
    model_config = {"from_attributes": True}