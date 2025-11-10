"""
Schemas para Vehículo Involucrado
"""

from pydantic import BaseModel, Field
from typing import Optional

class VehiculoBase(BaseModel):
    """Schema base de vehículo"""
    siniestro_id: int = Field(..., gt=0)
    tipo_vehiculo: str = Field(..., pattern="^(auto|moto|camion|camioneta|colectivo|bicicleta|peaton|objeto_fijo)$")
    marca: Optional[str] = None
    modelo: Optional[str] = None
    rol: str = Field(..., pattern="^(conductor|peaton|pasajero|otro)$")
    es_fallecido: bool = False

class VehiculoCreate(VehiculoBase):
    """Schema para crear vehículo"""
    pass

class VehiculoUpdate(BaseModel):
    """Schema para actualizar vehículo"""
    tipo_vehiculo: Optional[str] = Field(None, pattern="^(auto|moto|camion|camioneta|colectivo|bicicleta|peaton|objeto_fijo)$")
    marca: Optional[str] = None
    modelo: Optional[str] = None
    rol: Optional[str] = Field(None, pattern="^(conductor|peaton|pasajero|otro)$")
    es_fallecido: Optional[bool] = None

class VehiculoResponse(VehiculoBase):
    """Schema para respuesta de vehículo"""
    vehiculo_id: int
    
    model_config = {"from_attributes": True}