import os
import hashlib
from datetime import timedelta, datetime
from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from models.usuarios import Usuario
from database import get_db

# 🔐 Configuración desde variables de entorno
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

# 🚨 Verificación obligatoria de variables de entorno
if not ACCESS_TOKEN_EXPIRE_MINUTES or not SECRET_KEY or not ALGORITHM:
    raise RuntimeError("Faltan variables requeridas en el entorno (.env): ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, JWT_ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)

router = APIRouter()

# Función para hashear usando MD5 (solo se recomienda si las claves ya están así guardadas)
def hash_md5(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

@router.post("/login", response_model=dict)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.usuario == username).first()

    if not user or user.clave != hash_md5(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user.usuario, "exp": expire}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": user.usuario,
        "nombre": user.nombre,
        "apellido": user.apellido,
    }



@router.post("/registro", response_model=dict)
def registrar_usuario(
    nombre: str = Form(...),
    apellido: str = Form(...),
    usuario: str = Form(...),
    clave: str = Form(...),
    mail: str = Form(...),
    db: Session = Depends(get_db)
):
    # Verificar si ya existe un usuario con el mismo nombre de usuario o correo
    if db.query(Usuario).filter(Usuario.usuario == usuario).first():
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está en uso."
        )
    if db.query(Usuario).filter(Usuario.mail == mail).first():
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está en uso."
        )

    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        usuario=usuario,
        clave=hash_md5(clave),  # Se mantiene MD5 porque tu base ya lo usa así
        mail=mail
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario creado exitosamente.",
        "usuario_id": nuevo_usuario.id,
        "usuario": nuevo_usuario.usuario
    }
