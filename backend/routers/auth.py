"""
Router de autenticación
Endpoints: /auth/login, /auth/register, /auth/me
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from config.database import get_db
from config.settings import settings
from schemas.auth import Token, LoginRequest, RegisterRequest
from schemas.usuario import UsuarioResponse, UsuarioCreate
from services import auth as auth_service
from services import usuarios as usuarios_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# OAuth2 scheme para validar tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Dependency para obtener usuario actual desde el token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = auth_service.decodificar_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    usuario = await auth_service.obtener_usuario_por_email(db, email=token_data.email)
    if usuario is None:
        raise credentials_exception
    
    return usuario

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Login de usuario
    Retorna token JWT
    """
    usuario = await auth_service.autenticar_usuario(db, form_data.username, form_data.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.crear_access_token(
        data={"sub": usuario["email"], "rol": usuario["rol"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def register(
    usuario: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Registro de nuevo usuario
    """
    # Verificar si el email ya existe
    usuario_existente = await auth_service.obtener_usuario_por_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear usuario
    usuario_crear = UsuarioCreate(
        email=usuario.email,
        password=usuario.password,
        nombre=usuario.nombre,
        rol=usuario.rol
    )
    
    nuevo_usuario = await usuarios_service.crear_usuario(db, usuario_crear)
    return nuevo_usuario

@router.get("/me", response_model=UsuarioResponse)
async def obtener_perfil(
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    """
    Obtiene información del usuario actual
    """
    return usuario_actual