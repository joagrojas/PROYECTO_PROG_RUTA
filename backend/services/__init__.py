"""
Exportación de todos los servicios
"""

from . import auth
from . import usuarios
from . import avenidas
from . import tipos_siniestro
from . import siniestros
from . import vehiculos
from . import reportes

__all__ = [
    "auth",
    "usuarios",
    "avenidas",
    "tipos_siniestro",
    "siniestros",
    "vehiculos",
    "reportes"
]








