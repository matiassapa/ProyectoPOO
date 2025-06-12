from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class UsuarioHistorial(Base):
    __tablename__ = "usuarios_historial"

    id_usuario = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    id_historial = Column(Integer, ForeignKey("historial.id"), primary_key=True)
