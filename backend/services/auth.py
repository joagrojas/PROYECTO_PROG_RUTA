"""
Servicio de autenticación y manejo de JWT
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import settings
from schemas.auth import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Configuración de bcrypt para hashear passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Verifica si el password coincide con el hash"""
    return pwd_context.verify(password_plano, password_hash)

def hashear_password(password: str) -> str:
    """Genera hash bcrypt del password"""
    return pwd_context.hash(password)

def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

async def autenticar_usuario(db: AsyncSession, email: str, password: str):
    """Autentica usuario y devuelve sus datos si es correcto"""
    query = text("""
        SELECT id, email, password_hash, nombre, rol, activo
        FROM usuarios
        WHERE email = :email
    """)
    
    result = await db.execute(query, {"email": email})
    usuario = result.fetchone()
    
    if not usuario:
        return None
    
    if not usuario.activo:
        return None
    
    if not verificar_password(password, usuario.password_hash):
        return None
    
    # Actualizar último acceso
    update_query = text("""
        UPDATE usuarios
        SET ultimo_acceso = NOW()
        WHERE id = :id
    """)
    await db.execute(update_query, {"id": usuario.id})
    await db.commit()
    
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "rol": usuario.rol
    }

def decodificar_token(token: str) -> Optional[TokenData]:
    """Decodifica y valida token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        rol: str = payload.get("rol")
        
        if email is None:
            return None
        
        return TokenData(email=email, rol=rol)
    
    except JWTError:
        return None

async def obtener_usuario_por_email(db: AsyncSession, email: str):
    """Obtiene usuario por email"""
    query = text("""
        SELECT id, email, nombre, rol, activo, fecha_registro, ultimo_acceso
        FROM usuarios
        WHERE email = :email AND activo = 1
    """)
    
    result = await db.execute(query, {"email": email})
    usuario = result.fetchone()
    
    if not usuario:
        return None
    
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "rol": usuario.rol,
        "activo": usuario.activo,
        "fecha_registro": usuario.fecha_registro,
        "ultimo_acceso": usuario.ultimo_acceso
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Importar get_db aquí para usarlo en la dependencia
from config.database import get_db

async def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene el usuario actual desde el token JWT.
    
    Esta función es una "dependencia" de FastAPI que se usa en los endpoints.
    FastAPI la ejecuta automáticamente antes de cada endpoint que la requiera.
    
    Pasos que realiza:
    1. Decodifica el token JWT para extraer el email del usuario
    2. Busca el usuario completo en la base de datos usando ese email
    3. Valida que el usuario exista y esté activo
    4. Devuelve los datos completos del usuario (incluyendo id, email, nombre, rol)
    
    Args:
        token: Token JWT extraído del header "Authorization: Bearer <token>"
               FastAPI lo extrae automáticamente gracias a oauth2_scheme
        db: Sesión de base de datos, inyectada automáticamente por FastAPI
    
    Returns:
        dict: Diccionario con los datos del usuario:
              - id: ID numérico del usuario
              - email: Correo electrónico
              - nombre: Nombre completo
              - rol: Rol del usuario (admin, editor, consultor)
    
    Raises:
        HTTPException 401: Si el token es inválido, expiró, o el usuario no existe
    
    Ejemplo de uso en un endpoint:
        @router.post("/crear-algo")
        async def crear_algo(
            usuario_actual: dict = Depends(obtener_usuario_actual)
        ):
            # Aquí usuario_actual ya tiene: id, email, nombre, rol
            if usuario_actual["rol"] == "admin":
                # hacer algo...
    """
    # Validar que el token exista
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó token de autenticación",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Paso 1: Decodificar el token JWT para extraer el email
    # La función decodificar_token desencripta el token y extrae los datos
    token_data = decodificar_token(token)
    
    # Validar que el token sea válido y contenga un email
    if token_data is None or token_data.email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Paso 2: Buscar el usuario completo en la base de datos
    # Usamos el email que extrajimos del token para buscar en la BD
    usuario = await obtener_usuario_por_email(db, token_data.email)
    
    # Validar que el usuario exista y esté activo
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Paso 3: Devolver los datos completos del usuario
    # ¡IMPORTANTE! Ahora SÍ incluimos el campo "rol" que necesitan los endpoints
    return {
        "id": usuario["id"],
        "email": usuario["email"],
        "nombre": usuario["nombre"],
        "rol": usuario["rol"]
    }