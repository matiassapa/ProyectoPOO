from fastapi import APIRouter, HTTPException, Depends, Query, Request, Body, status
from typing import List, Dict, Optional, Literal
from math import ceil
from database.config import SessionLocal
from helpers.utils import check_consecutive_numbers, get_user_name_by_login, \
        parse_date, calculate_age, validar_correo, generar_codigo_para_link

from models.users import User, Role
import hashlib
import time

from datetime import datetime, timedelta, date
from database.config import get_db  # Importá get_db desde config.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import case, func, and_, or_, select, union_all, join, literal_column

from models.eventos_y_configs import Evento
from datetime import date
from security.security import get_current_user, require_roles, verify_api_key, get_password_hash


users_router = APIRouter() 



@users_router.get("/public-data", dependencies=[Depends(verify_api_key)])
def get_public_data():
    return {"message": "Este es un endpoint público accesible con API Key"}


@users_router.get("/profile")
def get_user_profile(current_user: dict = Depends(get_current_user)):
    return {"message": f"Bienvenido {current_user['user'].nombre}", "roles": current_user["role"]}


@users_router.get("/admin-data", dependencies=[Depends(verify_api_key), Depends(require_roles(["administrador"]))])
def get_admin_data():
    return {"message": "Solo los administradores pueden ver esto"}


@users_router.get("/reports", dependencies=[Depends(require_roles(["supervisor"]))])
def get_reports():
    return {"message": "Solo los supervisores pueden acceder a los reportes"}


@users_router.get("/user-access", dependencies=[Depends(require_roles(["agente", "supervisor"]))])
def user_access():
    return {"message": "Usuarios agentes y supervisores pueden acceder aquí"}


@users_router.get("/", response_model=dict, 
                  dependencies=[Depends( verify_api_key ), Depends(require_roles(["administrador", "supervisor"]))])
def get_users(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    role: Optional[Literal["administrador", "supervisor", "agente", "gestor", "conductor"]] = Query(None, description="Rol del usuario"),
    search: Optional[str] = Query(None, min_length=3, description="Búsqueda por al menos 3 caracteres"),
    fecha_alta_inicio: Optional[str] = Query(None, description="Fecha de alta inicio (AAAA-MM-DD)"),
    fecha_alta_fin: Optional[str] = Query(None, description="Fecha de alta fin (AAAA-MM-DD)")
):
    """
    Devuelve los usuarios de la tabla `users` paginados con filtros opcionales.
    """

    try:

        # Construcción de la consulta
        query = (
            db.query(
                User.login,
                User.nombre,
                User.apellido,
                User.celular,
                User.operativo,
                User.mail,
                User.calle_y_nro,
                User.barrio,
                User.localidad,
                User.provincia,
                User.fecha_alta,
                User.profesion,
                User.cargo,
                Role.description.label("role"),
            )
            .join(Role, User.role_id == Role.role_id, isouter=True)  # JOIN con Role (izquierdo para incluir usuarios sin rol)
        )

        # Filtro por fechas
        if fecha_alta_inicio or fecha_alta_fin:
            fecha_inicio = datetime.strptime(fecha_alta_inicio, "%Y-%m-%d") if fecha_alta_inicio else datetime(1970, 1, 1)
            fecha_fin = datetime.strptime(fecha_alta_fin, "%Y-%m-%d") if fecha_alta_fin else datetime.now()
            query = query.filter(User.fecha_alta.between(fecha_inicio, fecha_fin))

        # Filtro por rol
        if role:
            query = query.filter(Role.description.ilike(role.capitalize()))  # Ignora mayúsculas/minúsculas

        # Filtro de búsqueda
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (User.nombre.ilike(search_pattern)) |
                (User.apellido.ilike(search_pattern)) |
                (User.login.ilike(search_pattern)) |
                (User.mail.ilike(search_pattern)) |
                (User.celular.ilike(search_pattern)) |
                (User.calle_y_nro.ilike(search_pattern)) |
                (User.barrio.ilike(search_pattern)) |
                (User.localidad.ilike(search_pattern)) |
                (User.provincia.ilike(search_pattern))
            )

        # Obtener el número total de registros antes de paginar
        total_records = query.count()
        total_pages = max((total_records // limit) + (1 if total_records % limit > 0 else 0), 1)

        # Validar si la página solicitada existe
        if page > total_pages:
            return {"page": page, "limit": limit, "total_pages": total_pages, "total_records": total_records, "users": []}

        # Aplicar paginación
        skip = (page - 1) * limit
        users = query.offset(skip).limit(limit).all()

        # Construcción de la respuesta
        users_list = [
            {
                "login": user.login,
                "nombre": user.nombre or "",
                "apellido": user.apellido or "",
                "celular": user.celular or "",
                "operativo": user.operativo or "N",
                "mail": user.mail or "",
                "calle_y_nro": user.calle_y_nro or "",
                "barrio": user.barrio or "",
                "localidad": user.localidad or "",
                "provincia": user.provincia or "",
                "fecha_alta": user.fecha_alta.strftime("%Y-%m-%d") if user.fecha_alta else None,
                "profesion": user.profesion or "",
                "cargo": user.cargo or "",
                "role": user.role or "Sin rol asignado",                
            }
            for user in users
        ]

        return {
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "total_records": total_records,
            "users": users_list,
        }

    except SQLAlchemyError as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error al recuperar los usuarios: {str(e)}")



@users_router.post("/", status_code=201, 
                   dependencies=[Depends( verify_api_key ), Depends(require_roles(["administrador", "supervisor"]))])
def create_user(
    db: Session = Depends(get_db),
    login: str = Body(...),
    clave: str = Body(...),
    nombre: str = Body(...),
    apellido: Optional[str] = Body(None),
    celular: Optional[str] = Body(None),
    mail: Optional[str] = Body(None),
    fecha_nacimiento: Optional[date] = Body(None),
    profesion: Optional[str] = Body(None),
    cargo: Optional[str] = Body(None),
    role_name: Optional[str] = Body(None), 
):
    """
    Crea un nuevo usuario en la base de datos usando bcrypt para la contraseña.
    """

    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.login == login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # 🔍 Buscar el role_id por nombre
    role = db.query(Role).filter(Role.description == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    role_id = role.role_id

    # ✅ Encriptar clave antes de guardar usando bcrypt
    hashed_password = get_password_hash(clave)

    # Crear usuario
    new_user = User(
        login=login,
        clave=hashed_password, 
        nombre=nombre,
        apellido=apellido,
        celular=celular,
        mail=mail,
        fecha_nacimiento=fecha_nacimiento,
        active="Y",
        role_id=role_id,
        fecha_alta=date.today(),
        operativo="Y",
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")

    return {"message": "Usuario creado exitosamente", "user": {"login": login, "nombre": nombre}}