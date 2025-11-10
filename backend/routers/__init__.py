"""
Exportación de todos los routers
"""

from .auth import router as auth_router
from .usuarios import router as usuarios_router
from .avenidas import router as avenidas_router
from .tipos_siniestro import router as tipos_siniestro_router
from .siniestros import router as siniestros_router
from .vehiculos import router as vehiculos_router
from .reportes import router as reportes_router
from .reportes_delito import router as reportes_delito_router  # Nuevo router agregado

__all__ = [
    "auth_router",
    "usuarios_router",
    "avenidas_router",
    "tipos_siniestro_router",
    "siniestros_router",
    "vehiculos_router",
    "reportes_router",
    "reportes_delito_router"  # Exportar el nuevo router
]