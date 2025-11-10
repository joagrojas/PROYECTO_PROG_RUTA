"""
Schema Pydantic para Reportes Delictivos
Define la estructura y validación de datos para reportes de delitos
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime


# ========================================
# ENUMS para valores permitidos
# ========================================
# Estos valores deben coincidir con los ENUM de la base de datos

TIPOS_DELITO = ['robo', 'asalto', 'hurto', 'vandalismo', 'otro']
NIVELES_PELIGROSIDAD = ['baja', 'media', 'alta']


# ========================================
# SCHEMA BASE
# ========================================
class ReporteDelitoBase(BaseModel):
    """
    Clase base con los campos comunes de un reporte delictivo.
    Esta clase se usa como base para Create, Update y Response.
    """
    fecha: date = Field(..., description="Fecha del incidente delictivo")
    hora: time = Field(..., description="Hora del incidente")
    avenida_id: int = Field(..., gt=0, description="ID de la avenida donde ocurrió")
    tipo_delito: str = Field(..., description="Tipo de delito (robo, asalto, hurto, vandalismo, otro)")
    nivel_peligrosidad: str = Field(..., description="Nivel de peligrosidad (baja, media, alta)")
    descripcion: Optional[str] = Field(None, description="Descripción detallada del incidente")
    usuario_id: int = Field(..., gt=0, description="ID del usuario que registra el reporte")

    class Config:
        """Configuración del modelo Pydantic"""
        json_schema_extra = {
            "example": {
                "fecha": "2024-11-05",
                "hora": "20:30:00",
                "avenida_id": 1,
                "tipo_delito": "robo",
                "nivel_peligrosidad": "alta",
                "descripcion": "Robo a mano armada en intersección",
                "usuario_id": 1
            }
        }


# ========================================
# SCHEMA PARA CREAR (CREATE)
# ========================================
class ReporteDelitoCreate(ReporteDelitoBase):
    """
    Schema para crear un nuevo reporte delictivo.
    Incluye validaciones adicionales.
    """
    
    # Validación personalizada para tipo_delito
    @classmethod
    def validar_tipo_delito(cls, v):
        """Valida que el tipo de delito sea válido"""
        if v not in TIPOS_DELITO:
            raise ValueError(f'tipo_delito debe ser uno de: {", ".join(TIPOS_DELITO)}')
        return v
    
    # Validación personalizada para nivel_peligrosidad
    @classmethod
    def validar_nivel_peligrosidad(cls, v):
        """Valida que el nivel de peligrosidad sea válido"""
        if v not in NIVELES_PELIGROSIDAD:
            raise ValueError(f'nivel_peligrosidad debe ser uno de: {", ".join(NIVELES_PELIGROSIDAD)}')
        return v


# ========================================
# SCHEMA PARA ACTUALIZAR (UPDATE)
# ========================================
class ReporteDelitoUpdate(BaseModel):
    """
    Schema para actualizar un reporte delictivo existente.
    Todos los campos son opcionales (solo se actualizan los enviados).
    """
    fecha: Optional[date] = None
    hora: Optional[time] = None
    avenida_id: Optional[int] = Field(None, gt=0)
    tipo_delito: Optional[str] = None
    nivel_peligrosidad: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "nivel_peligrosidad": "media",
                "descripcion": "Descripción actualizada del incidente"
            }
        }


# ========================================
# SCHEMA DE RESPUESTA (OUTPUT)
# ========================================
class ReporteDelitoOut(ReporteDelitoBase):
    """
    Schema para la respuesta al listar reportes delictivos.
    Incluye campos adicionales como ID y nombre de avenida.
    """
    id: int = Field(..., description="ID único del reporte")
    fecha_registro: datetime = Field(..., description="Fecha de registro en el sistema")
    ultima_modificacion: Optional[datetime] = Field(None, description="Última modificación")
    # Campos adicionales del JOIN
    avenida_nombre: Optional[str] = Field(None, description="Nombre de la avenida")
    usuario_nombre: Optional[str] = Field(None, description="Nombre del usuario que registró")

    class Config:
        from_attributes = True  # Permite crear desde objetos ORM
        json_schema_extra = {
            "example": {
                "id": 1,
                "fecha": "2024-11-05",
                "hora": "20:30:00",
                "avenida_id": 1,
                "tipo_delito": "robo",
                "nivel_peligrosidad": "alta",
                "descripcion": "Robo a mano armada",
                "usuario_id": 1,
                "fecha_registro": "2024-11-05T15:30:00",
                "ultima_modificacion": "2024-11-05T15:30:00",
                "avenida_nombre": "Av. Perón",
                "usuario_nombre": "María González"
            }
        }


# ========================================
# SCHEMA DE RESPUESTA CON MENSAJE
# ========================================
class ReporteDelitoResponse(BaseModel):
    """
    Schema para respuesta de operaciones exitosas.
    Incluye un mensaje y los datos del reporte.
    """
    mensaje: str = Field(..., description="Mensaje de confirmación")
    reporte: ReporteDelitoOut

    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Reporte delictivo creado exitosamente",
                "reporte": {
                    "id": 1,
                    "fecha": "2024-11-05",
                    "hora": "20:30:00",
                    "tipo_delito": "robo",
                    "nivel_peligrosidad": "alta"
                }
            }
        }


# ========================================
# NOTAS TÉCNICAS (Para entender el código)
# ========================================
"""
1. ¿Por qué usamos Pydantic?
   - Validación automática de datos
   - Documentación automática en /docs
   - Conversión de tipos automática
   - Previene errores de tipo en tiempo de ejecución

2. ¿Qué es Field()?
   - Define validaciones adicionales (ej: gt=0 significa "mayor que 0")
   - Agrega descripciones que aparecen en la documentación
   - Permite valores por defecto

3. ¿Por qué separamos Create, Update y Out?
   - Create: Solo campos necesarios para crear (sin ID)
   - Update: Todos opcionales (solo se actualiza lo que viene)
   - Out: Incluye campos generados por la BD (ID, timestamps, JOINs)

4. ¿Qué es from_attributes = True?
   - Permite crear un schema desde objetos de base de datos
   - Necesario cuando usas SQLAlchemy o consultas SQL directas
"""