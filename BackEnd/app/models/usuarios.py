from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    clave = Column(String(64), nullable=False)  # MD5 son 32 caracteres en hex, usamos hasta 64 por seguridad
    mail = Column(String(100), unique=True, nullable=False)
