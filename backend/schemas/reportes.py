from pydantic import BaseModel
from typing import List, Optional

class ResumenGeneral(BaseModel):
    total_siniestros: int
    total_fallecidos: int
    total_heridos: int
    siniestros_graves: int
    siniestros_fin_semana: int

class SiniestrosPorZona(BaseModel):
    zona: str
    tipo_via: str
    total_siniestros: int
    total_fallecidos: int
    total_heridos: int
    promedio_victimas: float

class EstadisticasPorTipo(BaseModel):
    tipo_siniestro: str
    gravedad: str
    cantidad: int
    fallecidos: int
    heridos: int
    promedio_vehiculos: float
    siniestros_fin_semana: int
    porcentaje_fin_semana: float

class SiniestrosPorDia(BaseModel):
    dia_semana: str
    cantidad: int
    fallecidos: int
    heridos: int
    promedio_victimas: float

class AvenidaPeligrosa(BaseModel):
    nombre: str
    zona: str
    tipo: str
    total_siniestros: int
    total_fallecidos: int
    total_heridos: int
    clasificacion_riesgo: str

class AnalisisVehiculos(BaseModel):
    tipo_vehiculo: str
    siniestros_involucrados: int
    total_vehiculos: int
    fallecidos: int
    tasa_mortalidad: float
    siniestros_gravedad_alta: int

class SiniestrosPorMes(BaseModel):
    anio: int
    mes: int
    nombre_mes: str
    cantidad: int
    fallecidos: int
    heridos: int

class HorariosCriticos(BaseModel):
    hora: int
    cantidad: int
    fallecidos: int
    heridos: int
    clasificacion: str

class TopMarcas(BaseModel):
    marca: str
    cantidad: int
    con_fallecidos: int