import os
from datetime import datetime, timedelta
from typing import Any, Union, List
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database.config import get_db  # Importamos el acceso a la DB
from models.users import User, Role

# Cargar API_KEY desde el entorno
API_KEY = os.getenv("API_KEY")

# Cargar variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no está definido en el entorno. Configúralo en .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora

# Configuración para hash de contraseñas con Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurar esquema de autenticación con OAuth2 (Bearer Token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def verify_api_key(api_key: str = Header(None)):
    """Verifica que la API Key sea válida para endpoints públicos."""
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key no configurada en el servidor")

    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key inválida o no proporcionada")

    return True

def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    """
    Genera un token JWT con un tiempo de expiración.
    """
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash almacenado en bcrypt."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Devuelve el hash de la contraseña utilizando Bcrypt."""
    return pwd_context.hash(password)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtiene el usuario autenticado a partir del token JWT y su rol."""
    try:
        # Decodificar el token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_login: str = payload.get("sub")  
        if user_login is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token inválido"
            )

        # Buscar al usuario en la base de datos
        user = db.query(User).filter(User.login == user_login).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Usuario no encontrado"
            )

        # Obtener el rol del usuario (directamente desde `role_id`)
        role = db.query(Role.description).filter(Role.role_id == user.role_id).first()
        user_role = role.description if role else "Sin rol asignado"

        return {"user": user, "role": user_role}  # ✅ Devuelve usuario + rol único

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token inválido o expirado"
        )

def require_roles(allowed_roles: List[str]):
    """Dependencia para restringir el acceso a usuarios con ciertos roles."""
    def role_checker(current_user_data: dict = Depends(get_current_user)):
        user_roles = [current_user_data["role"]]  # Extraer el rol del usuario
        if not any(role in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso restringido a los roles permitidos: {', '.join(allowed_roles)}"
            )
        return current_user_data["user"]  # Devuelve el usuario si tiene permiso

    return role_checker
