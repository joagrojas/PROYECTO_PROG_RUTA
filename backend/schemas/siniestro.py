"""
Schemas para Siniestro
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

class SiniestroBase(BaseModel):
    """Schema base de siniestro"""
    fecha: Optional[date] = None
    hora: Optional[time] = None
    avenida_id: int
    tipo_id: int
    nivel_gravedad: Optional[str] = None
    victimas_fatales: Optional[int] = 0
    heridos: Optional[int] = 0
    num_vehiculos: Optional[int] = 0
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True  # pydantic v2: reemplaza orm_mode

class SiniestroCreate(SiniestroBase):
    """Schema para crear siniestro"""
    usuario_id: int = Field(..., gt=0)

class SiniestroUpdate(SiniestroBase):
    """Schema para actualizar siniestro"""
    pass

class SiniestroOut(SiniestroBase):
    """Schema para respuesta de siniestro"""
    id: int

# Alias para compatibilidad con cualquier import que espere SiniestroResponse
SiniestroResponse = SiniestroOut