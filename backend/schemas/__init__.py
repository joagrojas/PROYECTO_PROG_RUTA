"""
Exportación de todos los schemas
"""

from .auth import (
    Token,
    TokenData,
    LoginRequest,
    RegisterRequest,
    ChangePasswordRequest
)

from .usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioInDB
)

from .avenida import (
    AvenidaBase,
    AvenidaCreate,
    AvenidaUpdate,
    AvenidaResponse
)

from .tipo_siniestro import (
    TipoSiniestroBase,
    TipoSiniestroCreate,
    TipoSiniestroUpdate,
    TipoSiniestroResponse
)

from .siniestro import (
    SiniestroBase,
    SiniestroCreate, 
    SiniestroUpdate,
    SiniestroOut
)

from .vehiculo import (
    VehiculoBase,
    VehiculoCreate,
    VehiculoUpdate,
    VehiculoResponse
)

__all__ = [
    # Auth
    "Token",
    "TokenData",
    "LoginRequest",
    "RegisterRequest",
    "ChangePasswordRequest",
    
    # Usuario
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "UsuarioInDB",
    
    # Avenida
    "AvenidaBase",
    "AvenidaCreate",
    "AvenidaUpdate",
    "AvenidaResponse",
    
    # Tipo Siniestro
    "TipoSiniestroBase",
    "TipoSiniestroCreate",
    "TipoSiniestroUpdate",
    "TipoSiniestroResponse",
    
    # Siniestro
    "SiniestroBase",
    "SiniestroCreate",
    "SiniestroUpdate",
    "SiniestroOut",
    
    # Vehículo
    "VehiculoBase",
    "VehiculoCreate",
    "VehiculoUpdate",
    "VehiculoResponse",
]

