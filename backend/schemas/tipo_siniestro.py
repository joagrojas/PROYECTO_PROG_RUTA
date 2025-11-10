"""
Schemas para Tipo de Siniestro
"""

from pydantic import BaseModel, Field
from typing import Optional

class TipoSiniestroBase(BaseModel):
    """Schema base de tipo de siniestro"""
    nombre: str = Field(..., min_length=1, max_length=100)
    gravedad: str = Field(..., pattern="^(baja|media|alta)$")
    descripcion: Optional[str] = None

class TipoSiniestroCreate(TipoSiniestroBase):
    """Schema para crear tipo de siniestro"""
    pass

class TipoSiniestroUpdate(BaseModel):
    """Schema para actualizar tipo de siniestro"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    gravedad: Optional[str] = Field(None, pattern="^(baja|media|alta)$")
    descripcion: Optional[str] = None

class TipoSiniestroResponse(TipoSiniestroBase):
    """Schema para respuesta de tipo de siniestro"""
    id: int
    
    model_config = {"from_attributes": True}