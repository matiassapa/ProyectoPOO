from sqlalchemy import Column, Integer, String, DateTime, Enum
from models.base import Base


class Evento(Base):
    __tablename__ = "evento"

    evento_id = Column(Integer, primary_key=True, autoincrement=True)
    evento_detalle = Column(String(255), nullable=False)
    evento_fecha = Column(DateTime, nullable=True)
    login = Column(String(190), nullable=True)


class Settings(Base):
    __tablename__ = "settings"

    set_name = Column(String(255), primary_key=True)  # Clave primaria
    set_value = Column(String(255), nullable=True)  # Puede ser NULL
