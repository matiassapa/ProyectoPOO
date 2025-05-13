from fastapi import APIRouter, HTTPException, Depends, status, Form
from sqlalchemy.orm import Session
from database.config import get_db
from models.users import User, Role
from models.eventos_y_configs import Evento
from helpers.utils import check_consecutive_numbers
from datetime import timedelta, datetime
from security.security import verify_password, create_access_token, get_password_hash, verify_api_key
import os

login_router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))  # 1 hora por defecto

# 🔹 LOGIN con bcrypt
@login_router.post("/login", response_model=dict)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Verifica las credenciales del usuario usando bcrypt y devuelve un token de acceso.
    """

    user = db.query(User).filter(User.login == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario no encontrado."
        )

    # 🔹 Verificar la contraseña con bcrypt
    if not verify_password(password, user.clave):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Contraseña incorrecta."
        )

    # Obtener rol del usuario
    role = db.query(Role.description).filter(Role.role_id == user.role_id).first()
    role_name = role.description if role else "Sin rol asignado"

    # Generar token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=str(user.login), expires_delta=access_token_expires)

    # Registrar evento de login
    nuevo_evento = Evento(
        login=username,
        evento_detalle="Ingreso exitoso al sistema.",
        evento_fecha=datetime.now()
    )
    db.add(nuevo_evento)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "login": user.login,
        "name": user.nombre,
        "apellido": user.apellido,
        "email": user.mail,
        "role": role_name,
        "message": "Inicio de sesión exitoso"
    }


# 🔹 CAMBIO DE CONTRASEÑA con bcrypt
@login_router.post("/change-password", response_model=dict, dependencies=[Depends(verify_api_key)])
def change_password(
    username: str = Form(...),
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Permite a un usuario cambiar su contraseña si proporciona la contraseña actual correctamente.
    """

    user = db.query(User).filter(User.login == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # 🔹 Verificar la contraseña actual con bcrypt
    if not verify_password(old_password, user.clave):
        raise HTTPException(status_code=401, detail="La contraseña actual es incorrecta.")

    # Verificar que las contraseñas nuevas coincidan
    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail="Las contraseñas nuevas no coinciden.")

    # 🔹 Guardar la nueva contraseña en bcrypt
    user.clave = get_password_hash(new_password)
    db.commit()

    return {"message": "Contraseña cambiada exitosamente."}
