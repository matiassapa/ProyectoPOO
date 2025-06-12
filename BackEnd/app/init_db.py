import os
import hashlib
from database import Base, engine, SessionLocal
from models.usuarios import Usuario
from models.usuarios_historial import UsuarioHistorial

def hash_md5(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def init():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    if db.query(Usuario).first():
        print("Usuarios ya existen.")
        db.close()
        return

    # ✅ Obtener clave desde .env, y lanzar error si no está
    default_password = os.getenv("DEFAULT_USER_PASSWORD")
    if not default_password:
        raise RuntimeError("La variable DEFAULT_USER_PASSWORD no está definida en el entorno.")

    password_hashed = hash_md5(default_password)

    usuarios = [
        {"nombre": "Admin", "apellido": "Principal", "usuario": "admin", "mail": "admin@correo.com"},
        {"nombre": "Juana", "apellido": "Pérez", "usuario": "jperez", "mail": "jperez@correo.com"},
        {"nombre": "Luis", "apellido": "Martínez", "usuario": "lmartinez", "mail": "lmartinez@correo.com"},
        {"nombre": "Ana", "apellido": "Gómez", "usuario": "agomez", "mail": "agomez@correo.com"},
        {"nombre": "Mario", "apellido": "Rojas", "usuario": "mrojas", "mail": "mrojas@correo.com"},
    ]

    for u in usuarios:
        db.add(Usuario(
            nombre=u["nombre"],
            apellido=u["apellido"],
            usuario=u["usuario"],
            mail=u["mail"],
            clave=password_hashed
        ))

    db.commit()
    db.close()
    print("Usuarios cargados correctamente.")
