"""
Configuración de la aplicación usando Pydantic Settings
Lee variables desde .env
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Base de datos
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3309
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = "siniestros_viales"
    
    # Seguridad
    SECRET_KEY: str = "tu_clave_secreta_super_segura_cambiar_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Configuration - 
    API_TITLE: str = "Sistema de Gestión de Siniestros Viales"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Backend para el sistema de gestión de siniestros viales de La Rioja"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Debug
    DEBUG: bool = False
    
    # Configuración de Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()